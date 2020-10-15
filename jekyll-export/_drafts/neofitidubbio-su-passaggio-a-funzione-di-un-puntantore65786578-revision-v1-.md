---
id: 6582
date: 2016-08-23T14:51:50+02:00
author: ma
layout: revision
guid: http://www.italiancpp.org/2016/08/23/6578-revision-v1/
permalink: /2016/08/23/6578-revision-v1/
---
Grazie di nuovo.  
Quindi, credo di aver capito che la make_shared prenda come argomento un oggetto e mi restituisca un puntatore condiviso a quell&#8217;oggetto, e non, come ipotizzavo inizialmente, prenda come argomento un puntantore canonico e me ne resistuisca uno di tipo shared (e già sono soddisfatto).

Per quanto riguarda la ImageRvaToVa è definita nel DbgHelp.h, ignoro dove sia implementata e ignoro ancora di più cosa vorrebbe che facessi con il puntatore che mi restituisce. A riguardo, come posso scoprirlo?

giusto per spiegarmi meglio, la mia terminologia c++ lascia alquanto a desiderare, posto il codice, ma prima qualche spiegazione: ho preso un codice trovato in rete che faceva una parte dell&#8217;analisi del Portable Execution Format ed ho iniziato ad implementare alcuni pezzi mancanti(l&#8217;ottimizzazione, in termini di verifica delle risorse istanziate e loro distruzione, l&#8217;avrei eseguita una volta terminato).  
Al momento sono qui(le righe imputate sono le ultime del metodo DumpCOR20Header)

ConsoleAppPe01.cpp  
[cce_cpp]  
#include &#8220;stdafx.h&#8221;  
#include <windows.h>  
#include <stdio.h>  
#include <string.h>  
#include <time.h>  
#include <delayimp.h>  
#include <wintrust.h>  
#include <Dbghelp.h>  
#include <winnt.h>  
#include <iostream>  
#include <vector>  
#include <bitset>  
#include <memory>

#include &#8220;pe.h&#8221;

WORD\_VALUE\_NAMES g_arMachines[] =  
{  
{ IMAGE\_FILE\_MACHINE_UNKNOWN, &#8220;UNKNOWN&#8221; },  
{ IMAGE\_FILE\_MACHINE_I386, &#8220;I386&#8221; },  
{ IMAGE\_FILE\_MACHINE_R3000, &#8220;R3000&#8221; },  
{ IMAGE\_FILE\_MACHINE_R4000, &#8220;R4000&#8221; },  
{ IMAGE\_FILE\_MACHINE_R10000, &#8220;R10000&#8221; },  
{ IMAGE\_FILE\_MACHINE_WCEMIPSV2, &#8220;WCEMIPSV2&#8221; },  
{ IMAGE\_FILE\_MACHINE_ALPHA, &#8220;ALPHA&#8221; },  
{ IMAGE\_FILE\_MACHINE_SH3, &#8220;SH3&#8221; },  
{ IMAGE\_FILE\_MACHINE_SH3DSP, &#8220;SH3DSP&#8221; },  
{ IMAGE\_FILE\_MACHINE_SH3E, &#8220;SH3E&#8221; },  
{ IMAGE\_FILE\_MACHINE_SH4, &#8220;SH4&#8221; },  
{ IMAGE\_FILE\_MACHINE_SH5, &#8220;SH5&#8221; },  
{ IMAGE\_FILE\_MACHINE_ARM, &#8220;ARM&#8221; },  
{ IMAGE\_FILE\_MACHINE_THUMB, &#8220;THUMB&#8221; },  
{ IMAGE\_FILE\_MACHINE_AM33, &#8220;AM33&#8221; },  
{ IMAGE\_FILE\_MACHINE_POWERPC, &#8220;POWERPC&#8221; },  
{ IMAGE\_FILE\_MACHINE_POWERPCFP, &#8220;POWERPCFP&#8221; },  
{ IMAGE\_FILE\_MACHINE_IA64, &#8220;IA64&#8221; },  
{ IMAGE\_FILE\_MACHINE_MIPS16, &#8220;MIPS16&#8221; },  
{ IMAGE\_FILE\_MACHINE_ALPHA64, &#8220;ALPHA64&#8221; },  
{ IMAGE\_FILE\_MACHINE_MIPSFPU, &#8220;MIPSFPU&#8221; },  
{ IMAGE\_FILE\_MACHINE_MIPSFPU16, &#8220;MIPSFPU16&#8221; },  
{ IMAGE\_FILE\_MACHINE_TRICORE, &#8220;TRICORE&#8221; },  
{ IMAGE\_FILE\_MACHINE_CEF, &#8220;CEF&#8221; },  
{ IMAGE\_FILE\_MACHINE_EBC, &#8220;EBC&#8221; },  
{ IMAGE\_FILE\_MACHINE_AMD64, &#8220;AMD64&#8221; },  
{ IMAGE\_FILE\_MACHINE_M32R, &#8220;M32R&#8221; },  
{ IMAGE\_FILE\_MACHINE_CEE, &#8220;CEE&#8221; },  
};

PSTR GetMachineTypeName(WORD wMachineType)  
{  
for (unsigned i = 0; i < ARRAY\_SIZE(g\_arMachines); i++)  
if (wMachineType == g_arMachines[i].wValue)  
return PSTR(g_arMachines[i].pszName);

return PSTR(&#8220;unknown&#8221;);  
}

bool ValidateMemory(PeLoaded *peLoaded, LPCVOID ptr, size_t nSize)  
{  
if (!ptr || (LPBYTE)ptr < (LPBYTE)peLoaded->pMappedFileBase)  
return false;  
ULONGLONG nPos = ((LPBYTE)ptr &#8211; (LPBYTE)peLoaded->pMappedFileBase);  
if ((nPos + nSize) > peLoaded->FileSize.QuadPart)  
return false;  
return true;  
}

template <class T> PIMAGE\_SECTION\_HEADER GetEnclosingSectionHeader(DWORD rva, T* pNTHeader) // &#8216;T&#8217; == PIMAGE\_NT\_HEADERS  
{  
//printf(&#8220;GetEnclosingSectionHeader(rva=0x%08X) \n&#8221;, rva);  
PIMAGE\_SECTION\_HEADER section = IMAGE\_FIRST\_SECTION(pNTHeader);  
unsigned i;

for (i = 0; i < pNTHeader->FileHeader.NumberOfSections; i++, section++)  
{  
// This 3 line idiocy is because Watcom&#8217;s linker actually sets the  
// Misc.VirtualSize field to 0. (!!! &#8211; Retards&#8230;.!!!)  
DWORD size = section->Misc.VirtualSize;

if (0 == size)  
size = section->SizeOfRawData;

// Is the RVA within this section?  
if ((rva >= section->VirtualAddress) &&  
(rva < (section->VirtualAddress + size)))  
{  
//printf(&#8220;GetEnclosingSectionHeader(rva=0x%08X)=0x%08X \n&#8221;, rva, (intptr_t)section);  
return section;  
}  
}

//printf(&#8220;GetEnclosingSectionHeader(rva=0x%08X)=0 \n&#8221;, rva);  
return 0;  
}

template <class T> LPVOID GetPtrFromRVA(DWORD rva, T* pNTHeader, PBYTE imageBase) // &#8216;T&#8217; = PIMAGE\_NT\_HEADERS  
{  
//printf(&#8220;GetPtrFromRVA(rva=0x%08X) \n&#8221;, rva);  
//_ASSERTE(pNTHeader!=NULL);

if (!pNTHeader || !imageBase)  
{  
return NULL;  
}

PIMAGE\_SECTION\_HEADER pSectionHdr;  
INT delta;  
pSectionHdr = GetEnclosingSectionHeader(rva, pNTHeader);

if (!pSectionHdr)  
return 0;

delta = (INT)(pSectionHdr->VirtualAddress &#8211; pSectionHdr->PointerToRawData);  
//printf(&#8220;GetPtrFromRVA(rva=0x%08X) -> (delta=%i) \n&#8221;, (DWORD)(rva &#8211; delta), delta);  
return (PVOID)(imageBase + rva &#8211; delta);  
}

template <class T> LPVOID GetPtrFromVA(PVOID ptr, T* pNTHeader, PBYTE pImageBase) // &#8216;T&#8217; = PIMAGE\_NT\_HEADERS  
{  
// Yes, under Win64, we really are lopping off the high 32 bits of a 64 bit  
// value. We&#8217;ll knowingly believe that the two pointers are within the  
// same load module, and as such, are RVAs  
DWORD rva = PtrToLong((PBYTE)ptr &#8211; pNTHeader->OptionalHeader.ImageBase);

return GetPtrFromRVA(rva, pNTHeader, pImageBase);  
}

void DisplayDataDirectoryEntry(PeLoaded \*peLoaded, const char \* pszName, IMAGE\_DATA\_DIRECTORY & dataDirEntry)  
{

if (dataDirEntry.VirtualAddress) {

TCHAR szRVA[12], szSize[12];  
printf((const char *)szRVA, &#8220;0x%08X&#8221;, dataDirEntry.VirtualAddress);  
printf((const char *)szSize, &#8220;0x%08X&#8221;, dataDirEntry.Size);

LPVOID ptr = NULL;  
if (peLoaded->Is64Bit)  
ptr = GetPtrFromRVA(dataDirEntry.VirtualAddress, peLoaded->pNTHeader64, peLoaded->pMappedFileBase);  
else  
ptr = GetPtrFromRVA(dataDirEntry.VirtualAddress, peLoaded->pNTHeader32, peLoaded->pMappedFileBase);

}  
printf(&#8221; %-16s rva: %08X size: %08X\n&#8221;, pszName, dataDirEntry.VirtualAddress, dataDirEntry.Size);  
}

void GetStreamHeaders(char *ui8BaseAddress, int &ui16Length, std::vector<StreamHeader> &lStreamHeader, int streams)  
{  
StreamHeader streamHeader;

for (int i = 0; i < streams; i++)  
{  
streamHeader.offset = \*reinterpret_cast<int \*>(ui8BaseAddress + ui16Length);  
ui16Length += 4;

streamHeader.size = \*reinterpret_cast<int \*>(ui8BaseAddress + ui16Length);  
ui16Length += 4;  
int j = 0;

for (; *(ui8BaseAddress + ui16Length + j) != 0; j++)  
{  
streamHeader.name.append(1, *(ui8BaseAddress + ui16Length + j));  
}  
if (((j + 1) % 4) != 0)  
ui16Length += (j + 1) + 4 &#8211; ((j + 1) % 4);  
else  
ui16Length += (j + 1);

lStreamHeader.push_back(streamHeader);  
streamHeader.name.clear();  
}  
}

StreamHeader * GetMetaData(std::vector<StreamHeader> &lStreamHeader, std::string str)  
{  
for (std::vector<StreamHeader>::iterator iteHeader = lStreamHeader.begin();  
iteHeader != lStreamHeader.end(); iteHeader++)  
{  
if (!strcmp((*iteHeader).name.c\_str(), str.c\_str()))  
{  
return &(*iteHeader);  
}  
}  
return nullptr;  
}

template <class T> void DumpCOR20Header(PeLoaded \*peLoaded, PBYTE pImageBase, T\* pNTHeader) // T = PIMAGE\_NT\_HEADERS  
{  
DWORD cor20HdrRVA; // COR20_HEADER RVA

cor20HdrRVA = GetImgDirEntryRVA(pNTHeader, IMAGE\_DIRECTORY\_ENTRY\_COM\_DESCRIPTOR);  
if (!cor20HdrRVA)  
return;

PIMAGE\_COR20\_HEADER pCor20Hdr = (PIMAGE\_COR20\_HEADER)GetPtrFromRVA(cor20HdrRVA, pNTHeader, pImageBase);

printf(&#8220;\n\*****\*\\*\* <.NET Runtime Header>: \*\*\***\*** \n\n&#8221;);

peLoaded->netRuntime.cb = pCor20Hdr->cb;  
peLoaded->netRuntime.MajorRuntimeVersion = pCor20Hdr->MajorRuntimeVersion;  
peLoaded->netRuntime.MinorRuntimeVersion = pCor20Hdr->MinorRuntimeVersion;  
peLoaded->netRuntime.Flags = pCor20Hdr->Flags;

peLoaded->netRuntime.MetaData = pCor20Hdr->MetaData;  
peLoaded->netRuntime.Resources = pCor20Hdr->Resources;  
peLoaded->netRuntime.StrongNameSignature = pCor20Hdr->StrongNameSignature;  
peLoaded->netRuntime.CodeManagerTable = pCor20Hdr->CodeManagerTable;  
peLoaded->netRuntime.VTableFixups = pCor20Hdr->VTableFixups;  
peLoaded->netRuntime.ExportAddressTableJumps = pCor20Hdr->ExportAddressTableJumps;  
peLoaded->netRuntime.ManagedNativeHeader = pCor20Hdr->ManagedNativeHeader;

printf(&#8221; Size: %u\n&#8221;, peLoaded->netRuntime.cb);  
printf(&#8221; Version: %u.%u\n&#8221;, peLoaded->netRuntime.MajorRuntimeVersion, peLoaded->netRuntime.MinorRuntimeVersion);  
printf(&#8221; Flags: %X\n&#8221;, peLoaded->netRuntime.Flags);  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_ILONLY) printf(&#8221; ILONLY\n&#8221;);  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_32BITREQUIRED) printf(&#8221; 32BITREQUIRED\n&#8221;);  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_IL\_LIBRARY) printf(&#8221; IL\_LIBRARY\n&#8221;);  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_STRONGNAMESIGNED) printf(&#8221; STRONGNAMESIGNED\n&#8221;);  
//if ( pCor20Hdr->Flags & ReplacesCorHdrNumericDefinesCustom::COMIMAGE\_FLAGS\_NATIVE\_ENTRYPOINT ) printf( &#8221; NATIVE\_ENTRYPOINT\n&#8221; );  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_NATIVE\_ENTRYPOINT) printf(&#8221; NATIVE\_ENTRYPOINT\n&#8221;);  
if (peLoaded->netRuntime.Flags & COMIMAGE\_FLAGS\_TRACKDEBUGDATA) printf(&#8221; TRACKDEBUGDATA\n&#8221;);  
DisplayDataDirectoryEntry(peLoaded, &#8220;MetaData&#8221;, peLoaded->netRuntime.MetaData);  
DisplayDataDirectoryEntry(peLoaded, &#8220;Resources&#8221;, peLoaded->netRuntime.Resources);  
DisplayDataDirectoryEntry(peLoaded, &#8220;StrongNameSig&#8221;, peLoaded->netRuntime.StrongNameSignature);  
DisplayDataDirectoryEntry(peLoaded, &#8220;CodeManagerTable&#8221;, peLoaded->netRuntime.CodeManagerTable);  
DisplayDataDirectoryEntry(peLoaded, &#8220;VTableFixups&#8221;, peLoaded->netRuntime.VTableFixups);  
DisplayDataDirectoryEntry(peLoaded, &#8220;ExprtAddrTblJmps&#8221;, peLoaded->netRuntime.ExportAddressTableJumps);  
DisplayDataDirectoryEntry(peLoaded, &#8220;ManagedNativeHdr&#8221;, peLoaded->netRuntime.ManagedNativeHeader);

PIMAGE\_NT\_HEADERS pImageNtHeader = ImageNtHeader(peLoaded->pMappedFileBase);  
char \* pMetaDataAddressChar = reinterpret_cast<char \*>(ImageRvaToVa(pImageNtHeader, peLoaded->pMappedFileBase, pCor20Hdr->MetaData.VirtualAddress, 0));  
std::shared\_ptr<char> pMetaDataAddress = std::make\_shared<char>(pMetaDataAddressChar); // static\_cast<std::shared\_ptr<char>>(ImageRvaToVa(pImageNtHeader, peLoaded->pMappedFileBase, pCor20Hdr->MetaData.VirtualAddress, 0));  
int mdSignature = \*(reinterpret_cast<int \*>(*pMetaDataAddress));

short majorVersion = \*(reinterpret_cast<short \*>(*pMetaDataAddress + 4));  
short minorVersion = \*(reinterpret_cast<short \*>(*pMetaDataAddress + 6));  
int reserved = \*(reinterpret_cast<int \*>(*pMetaDataAddress + 8));  
int length = \*(reinterpret_cast<int \*>(*pMetaDataAddress + 12));

std::string version;

for (int i = 16; i < (length + 16); i++)  
{  
version.append(1, \*(reinterpret_cast<char \*>(*pMetaDataAddress + i)));  
}

int reserved2 = \*(reinterpret_cast<short \*>(*pMetaDataAddress + 16 + length));  
int streams = \*(reinterpret_cast<short \*>(*pMetaDataAddress + 18 + length));  
int i16Length = 20 + length;  
std::vector<StreamHeader> lStreamHeader;

GetStreamHeaders(pMetaDataAddress.get(), i16Length, lStreamHeader, streams);

////now read the strings

//std::shared\_ptr<char> pStringsStream = std::make\_shared<char>(pMetaDataAddress.get() + GetMetaData(lStreamHeader, &#8220;#Strings&#8221;)->offset);  
//std::shared\_ptr<char\*> pStringsStream2 = std::make\_shared<char\*>(pMetaDataAddress.get() + GetMetaData(lStreamHeader, &#8220;#Strings&#8221;)->offset);

//peLoaded->netRuntime.pStringsStream = std::make_shared<char*>(pMetaDataAddress.get() + GetMetaData(lStreamHeader, &#8220;#Strings&#8221;)->offset);  
//peLoaded->netRuntime.pBlobStream = std::make_shared<char>(pMetaDataAddress.get() + GetMetaData(lStreamHeader, &#8220;#Blob&#8221;)->offset);  
//peLoaded->netRuntime.pUSStream = std::make_shared<char>(pMetaDataAddress.get() + GetMetaData(lStreamHeader, &#8220;#US&#8221;)->offset);

}

bool DumpExeFilePE(PeLoaded *peLoaded, PIMAGE\_DOS\_HEADER dosHeader, PIMAGE\_NT\_HEADERS32 pNTHeader) {  
PBYTE pImageBase = (PBYTE)dosHeader;  
PIMAGE\_NT\_HEADERS64 pNTHeader64;

pNTHeader64 = (PIMAGE\_NT\_HEADERS64)pNTHeader;

peLoaded->Machine = pNTHeader->FileHeader.Machine;  
bool bIs64Bit = (pNTHeader->OptionalHeader.Magic == IMAGE\_NT\_OPTIONAL\_HDR64\_MAGIC);  
peLoaded->Is64Bit = bIs64Bit;  
peLoaded->ArchitectureBitsNumber = (bIs64Bit) ? 64 : 32;

if (peLoaded->Is64Bit)  
{  
peLoaded->pNTHeader64 = pNTHeader64;  
}  
else  
{  
peLoaded->pNTHeader32 = pNTHeader; // (PIMAGE\_NT\_HEADERS32)pNTHeader;  
}

printf(&#8220;\n\***\*****\*\\*\* COR20Header \*\*\***\***\***\n\n&#8221;);  
peLoaded->Is64Bit  
? DumpCOR20Header(peLoaded, pImageBase, pNTHeader64)  
: DumpCOR20Header(peLoaded, pImageBase, pNTHeader);

printf(&#8220;\n\n&#8221;);

return true;

}

bool DumpExeFile(PeLoaded *peLoaded, PIMAGE\_DOS\_HEADER dosHeader) {  
bool lbSucceeded = false;  
PIMAGE\_NT\_HEADERS32 pNTHeader;  
PBYTE pImageBase = (PBYTE)dosHeader;

// Make pointers to 32 and 64 bit versions of the header.  
pNTHeader = MakePtr(PIMAGE\_NT\_HEADERS32, dosHeader,  
dosHeader->e_lfanew);

//pNTHeader = (PIMAGE\_NT\_HEADERS32) ( (intptr\_t) dosHeader + (intptr\_t) dosHeader->e_lfanew);

DWORD nSignature = 0;  
if (ValidateMemory(peLoaded, pNTHeader, sizeof(pNTHeader->Signature)))  
{  
nSignature = pNTHeader->Signature;  
if (nSignature == IMAGE\_NT\_SIGNATURE)  
{  
lbSucceeded = DumpExeFilePE(peLoaded, dosHeader, pNTHeader);  
}  
}  
return lbSucceeded;  
}

bool DumpFile(PeLoaded \*peLoaded, LPBYTE pFileData, \_\_int64 nFileSize/\*mapped*/, \_\_int64 nFullFileSize) {  
bool lbSucceeded = false;  
PIMAGE\_DOS\_HEADER dosHeader;  
peLoaded->pNTHeader32 = NULL;  
peLoaded->pNTHeader64 = NULL;  
peLoaded->Is64Bit = false;  
peLoaded->FileSize.QuadPart = nFileSize;  
peLoaded->FileFullSize.QuadPart = nFullFileSize;  
peLoaded->pMappedFileBase = pFileData;  
dosHeader = (PIMAGE\_DOS\_HEADER)peLoaded->pMappedFileBase;

if (dosHeader->e\_magic == IMAGE\_DOS_SIGNATURE) {  
lbSucceeded = DumpExeFile(peLoaded, dosHeader);  
}

return lbSucceeded;  
}

int main()  
{  
HANDLE hFile;  
BYTE *BaseAddress;  
size_t FileSize;  
LPBYTE pFileData = NULL;  
HANDLE hFileMapping;

wchar\_t buffer[MAX\_PATH];

GetModuleFileName(NULL, buffer, MAX_PATH);  
printf(&#8220;%s&#8221;, buffer);

printf(&#8220;\nOpening File&#8230;\n&#8221;);

hFile = CreateFile((LPCWSTR)L&#8221;D:\\WORK\\VisualStudio2015\\ConsoleAppPE00\\Debug\\testfiles\\PeConsoleTest2.exe&#8221;,  
//hFile = CreateFile(&#8220;./testfiles/PeNetTest.dll&#8221;,  
GENERIC\_READ, FILE\_SHARE_READ, 0,  
//GENERIC\_READ | GENERIC\_WRITE, FILE\_SHARE\_READ, 0,  
OPEN\_EXISTING, FILE\_ATTRIBUTE_NORMAL, 0);

if (hFile == INVALID\_HANDLE\_VALUE)  
{  
printf(&#8220;Cannot Open the File\n&#8221;);  
return -1;  
}

BYTE Signature[2]; DWORD nRead = 0;  
LARGE_INTEGER nSize = { { 0 } };  
LARGE_INTEGER nFullSize = { { 0 } };

PeLoaded peLoaded;

peLoaded.FileSize.LowPart = GetFileSize(hFile, &peLoaded.FileSize.HighPart);

if (GetFileSizeEx(hFile, &nSize) && (nSize.QuadPart > 512)  
&& ReadFile(hFile, Signature, 2, &nRead, NULL)  
&& (Signature[0] == &#8216;M&#8217; && Signature[1] == &#8216;Z&#8217;))  
{

printf(&#8220;Valid DOS signature\n&#8221;);

BOOL lbSucceeded = TRUE;  
LARGE_INTEGER liPos, liTest;  
IMAGE\_DOS\_HEADER dosHeader = { 0 };  
IMAGE\_NT\_HEADERS64 NTHeader64 = { 0 };

nFullSize.QuadPart = nSize.QuadPart;  
dosHeader.e\_magic = IMAGE\_DOS_SIGNATURE;  
lbSucceeded = ReadFile(hFile, 2 + (LPBYTE)&dosHeader, sizeof(dosHeader) &#8211; 2, &nRead, NULL);

if (lbSucceeded)  
{  
printf(&#8220;ReadFile ok\n&#8221;);  
liPos.QuadPart = dosHeader.e_lfanew;  
lbSucceeded = (liPos.QuadPart >= sizeof(dosHeader) && liPos.QuadPart < nSize.QuadPart);  
}

if (lbSucceeded)  
{  
lbSucceeded = SetFilePointerEx(hFile, liPos, &liTest, FILE_BEGIN)  
&& ReadFile(hFile, &NTHeader64, sizeof(NTHeader64), &nRead, NULL)  
&& (NTHeader64.Signature == IMAGE\_NT\_SIGNATURE  
|| (NTHeader64.Signature & 0xFFFF) == IMAGE\_OS2\_SIGNATURE);  
// || (NTHeader64.Signature & 0xFFFF) == IMAGE\_OS2\_SIGNATURE_LE); &#8211; SMARTDRV.EXE, ??? ?? win  
printf(&#8220;SetFilePointerEx ok\n&#8221;);  
}

if (lbSucceeded)  
{

if (NTHeader64.Signature == IMAGE\_NT\_SIGNATURE)  
{  
if (NTHeader64.OptionalHeader.Magic == IMAGE\_NT\_OPTIONAL\_HDR64\_MAGIC)  
{  
if (NTHeader64.OptionalHeader.SizeOfImage < nSize.QuadPart)  
nSize.QuadPart = NTHeader64.OptionalHeader.SizeOfImage;  
}  
else  
{  
PIMAGE\_NT\_HEADERS32 pNTHeader32 = (PIMAGE\_NT\_HEADERS32)&NTHeader64;  
if (pNTHeader32->OptionalHeader.SizeOfImage < nSize.QuadPart)  
nSize.QuadPart = pNTHeader32->OptionalHeader.SizeOfImage;  
}  
}  
else  
{  
// ??? ?????? ????? 16?????? exe/dll, ??? ???-?? ??????, ? ??????? OS2  
}  
if (nSize.QuadPart >(256 << 20)) // ?????? ?? ?????? 256Mb  
nSize.QuadPart = (256 << 20);  
}

if (lbSucceeded)  
{  
hFileMapping = CreateFileMapping(hFile, NULL, PAGE_READONLY, 0, 0, NULL);  
//hFileMapping = CreateFileMapping(hFile, NULL, PAGE_READWRITE, 0, 0, NULL);  
lbSucceeded = (hFileMapping != NULL);  
}

if (lbSucceeded)  
{  
pFileData = (PBYTE)MapViewOfFile(hFileMapping, FILE\_MAP\_READ, 0, 0, nSize.LowPart);  
//pFileData = (PBYTE)MapViewOfFile(hFileMapping,FILE\_MAP\_WRITE,0,0,nSize.LowPart);  
lbSucceeded = (pFileData != NULL);  
}

if (lbSucceeded)  
{

DumpFile(&peLoaded, pFileData, nSize.QuadPart, nFullSize.QuadPart);  
}

}  
else {  
printf(&#8220;wrong signature&#8221;);  
}

UnmapViewOfFile(pFileData);  
CloseHandle(hFileMapping);  
CloseHandle(hFile);

std::cin.get();

return 0;  
}  
[/cce_cpp]

stdafx.h:  
[cce_cpp]  
#pragma once

#ifdef \_MSC\_VER  
#define \_CRT\_SECURE\_NO\_WARNINGS  
#endif

#include &#8220;targetver.h&#8221;

#include <stdio.h>  
//#include <tchar.h>  
#include <windows.h>  
#include <string>

#pragma comment(lib, &#8220;dbghelp.lib&#8221;)

#define FREE(p) HeapFree(GetProcessHeap(), 0, p)

// MakePtr is a macro that allows you to easily add to values (including  
// pointers) together without dealing with C&#8217;s pointer arithmetic. It  
// essentially treats the last two parameters as DWORDs. The first  
// parameter is used to typecast the result to the appropriate pointer type.  
//#define MakePtr( cast, ptr, addValue ) (cast)( (DWORD)(ptr) + (DWORD)(addValue))  
#define MakePtr( cast, ptr, addValue ) (cast)( (intptr\_t)(ptr) + (intptr\_t)(addValue))

#ifdef \_\_GNUC\_\_  
#define __try  
#define __except(a) if(0)  
#endif // \_\_GNUC\_\_

#ifndef IMAGE\_SIZEOF\_NT\_OPTIONAL64\_HEADER  
#define IMAGE\_SIZEOF\_NT\_OPTIONAL64\_HEADER 240  
#endif // IMAGE\_SIZEOF\_NT\_OPTIONAL64\_HEADER

#ifndef IMAGE\_SIZEOF\_NT\_OPTIONAL32\_HEADER  
#define IMAGE\_SIZEOF\_NT\_OPTIONAL32\_HEADER 224  
#endif // IMAGE\_SIZEOF\_NT\_OPTIONAL32\_HEADER

// typedef enum ReplacesCorHdrNumericDefinesCustom  
// {  
// // COM+ Header entry point flags.  
// // COMIMAGE\_FLAGS\_ILONLY =0x00000001,  
// // COMIMAGE\_FLAGS\_32BITREQUIRED =0x00000002,  
// // COMIMAGE\_FLAGS\_IL_LIBRARY =0x00000004,  
// // COMIMAGE\_FLAGS\_STRONGNAMESIGNED =0x00000008,  
// // DDBLD &#8211; Added Next Line &#8211; Still verifying general usage  
// COMIMAGE\_FLAGS\_NATIVE_ENTRYPOINT =0x00000010,  
// // DDBLD &#8211; End of Add  
// // COMIMAGE\_FLAGS\_TRACKDEBUGDATA =0x00010000,

// // Other kinds of flags follow

// } ReplacesCorHdrNumericDefinesCustom;

enum tag_PeStrMagics  
{  
ePeStr_Info = 0x1005,  
};

enum tag_PeStrFlags  
{  
PE_Far1 = 0x0001,  
PE_Far2 = 0x0002,  
PE_Far3 = 0x0004,  
PE_DOTNET = 0x0100,  
PE_UPX = 0x0200,  
PE\_VER\_EXISTS = 0x0400,  
PE\_ICON\_EXISTS = 0x0800,  
PE_SIGNED = 0x1000,  
};

struct PEData  
{  
DWORD nMagic;  
BOOL bValidateFailed;  
int nBits; // x16/x32/x64  
UINT nFlags; // tag_PeStrFlags  
wchar_t szExtension[32];  
wchar_t *szVersion, szVersionN[32], szVersionF[128], szVersionP[128];  
wchar_t szProduct[128];  
wchar_t szCompany[128]; // ??? company, ??? copyright?  
wchar_t szInfo[512]; // ?????? ??????????  
//  
PBYTE pMappedFileBase;  
ULARGE_INTEGER FileSize;  
ULARGE_INTEGER FileFullSize;  
PIMAGE\_NT\_HEADERS32 pNTHeader32;  
PIMAGE\_NT\_HEADERS64 pNTHeader64;  
bool bIs64Bit;  
WORD Machine;

PEData()  
{  
nMagic = ePeStr_Info; nBits = 0; nFlags = 0; bValidateFailed = FALSE; Machine = 0;  
szInfo[0] = szVersionN[0] = szProduct[0] = szCompany[0] = szExtension[0] = szVersionP[0] = szVersionF[0] = 0;  
szVersion = szVersionN;  
pMappedFileBase = NULL; FileSize.QuadPart = 0; pNTHeader32 = NULL; pNTHeader64 = NULL; bIs64Bit = false;  
FileFullSize.QuadPart = 0;  
};

void Close()  
{  
FREE(this);  
};  
};

typedef struct  
{  
WORD flag;  
//PSTR name;  
char const * name;  
} WORD\_FLAG\_DESCRIPTIONS;

typedef struct  
{  
WORD wValue;  
//PSTR pszName;  
char const * pszName;  
} WORD\_VALUE\_NAMES;

struct StreamHeader  
{  
int offset;  
int size;  
std::string name;  
};

struct TypeDef  
{  
int iFlag;  
int iTypeName;  
int iTypeNameSpace;  
int iExtends;  
int iFieldList;  
int iMethodList;  
};

struct MethodDef  
{  
int iRVA;  
short iImplFlags;  
short iFlags;  
int iName;  
int iSignature;  
int iParamList;  
};

struct Param  
{  
short iFlags;  
short iSequence;  
int iName;  
};

struct Field  
{  
short iFlag;  
int iName;  
int iSignature;  
};

struct Constant  
{  
short iType;  
int iParent;  
int iValue;  
};

#define NUMBER\_DLL\_CHARACTERISTICS (sizeof(DllCharacteristics) / sizeof(WORD\_FLAG\_DESCRIPTIONS))

#define NUMBER\_IMAGE\_DIRECTORY_ENTRYS (sizeof(ImageDirectoryNames)/sizeof(char *))

#define ARRAY_SIZE( x ) (sizeof(x) / sizeof(x[0]))

#define NUMBER\_IMAGE\_HEADER\_FLAGS (sizeof(ImageFileHeaderCharacteristics) / sizeof(WORD\_FLAG_DESCRIPTIONS))

#define GetImgDirEntryRVA( pNTHdr, IDE ) (pNTHdr->OptionalHeader.DataDirectory[IDE].VirtualAddress)

#define GetImgDirEntrySize( pNTHdr, IDE ) (pNTHdr->OptionalHeader.DataDirectory[IDE].Size)

[/cce_cpp]

pe.h  
[cce_cpp]  
#pragma once  
#include <windows.h>  
#include <string.h>  
#include <vector>  
#include <memory> 

class FieldDefinition {  
public:  
short iFlag;  
int iName;  
int iSignature;

std::string FieldNme;  
};

class MethodSectionClauseBase {  
public:  
int ClassToken;  
int FilterOffset;  
};

class MethodSectionClauseTiny : public MethodSectionClauseBase {  
public:  
short Flags;  
short TryOffset;  
char TryLength;  
short HandlerOffset;  
char HandlerLength;  
};

class MethodSectionClauseFat :public MethodSectionClauseBase {  
public:  
unsigned int Flags;  
unsigned int TryOffset;  
unsigned int TryLength;  
unsigned int HandlerOffset;  
unsigned int HandlerLength;  
};

class MethodSectionBase {  
public:  
unsigned char Kind;

MethodSectionBase() {};  
virtual ~MethodSectionBase() {};  
};

class MethodSectionTiny : public MethodSectionBase {  
public:  
unsigned char DataSize; // Size of the data for the block, including the header, say n*12+4.  
unsigned short Reserved;  
std::vector<MethodSectionClauseTiny*> Clauses;

};

class MethodSectionFat : public MethodSectionBase {  
public:  
unsigned int DataSize; // Size of the data for the block, including the header, say n*24+4.  
std::vector<MethodSectionClauseFat*> Clauses;  
};

class MethodDefinition {  
public:  
int iRVA;  
short iImplFlags;  
short iFlags;  
int iName;  
int iSignature;  
int iParamList;

bool FatHeader;  
char FirstByte;  
//char * FirstBytePosition;  
std::shared_ptr<char> FirstBytePosition;  
int HeaderSize;  
unsigned int MaxStack;  
unsigned int CodeSize;  
unsigned int LocalVarSigTok;  
std::string MethodName;  
int ParamListIndex;

std::string BodyBytes;  
std::vector<MethodSectionBase*> Sections;  
};

class TypeDefinition  
{  
public:  
int iFlag;  
int iTypeName;  
int iTypeNameSpace;  
int iExtends;  
int iFieldList;  
int iMethodList;

std::string ModuleName;  
std::string TypeNamespace;  
std::string Field;  
std::string Methods;  
std::string Extends;  
};

class ConstantDefinition {  
public:  
int iParent;  
int iValue;  
int iType;  
std::string Value;  
};

class NetRuntime {  
public:  
DWORD cb; //Size of this structure (0x48)  
WORD MajorRuntimeVersion; //Major version of the CLR runtime  
WORD MinorRuntimeVersion; //Minor version of the CLR runtime  
IMAGE\_DATA\_DIRECTORY MetaData; //RVA to, and size of, the executables meta-data  
DWORD Flags; //Bitwise flags indicating attributes of this executable

union  
{  
DWORD EntryPointToken; //If COMIMAGE\_FLAGS\_NATIVE_ENTRYPOINT not set; EntryPointToken represents a managed entry point.  
DWORD EntryPointRVA; //If COMIMAGE\_FLAGS\_NATIVE_ENTRYPOINT set; EntryPointRVA represents a RVA to a native entry point.  
} DUMMYUNIONNAME;

IMAGE\_DATA\_DIRECTORY Resources; //RVA to, and size of, the executables resources  
IMAGE\_DATA\_DIRECTORY StrongNameSignature;  
IMAGE\_DATA\_DIRECTORY CodeManagerTable; //Always 0  
IMAGE\_DATA\_DIRECTORY VTableFixups; //Contains the location and size of an array of VtableFixups  
IMAGE\_DATA\_DIRECTORY ExportAddressTableJumps; //Always 0  
IMAGE\_DATA\_DIRECTORY ManagedNativeHeader; //Always 0

char HeapOffSetSize;

//char * pStringsStream;  
std::shared_ptr<char*> pStringsStream;  
//char * pBlobStream;  
std::shared_ptr<char> pBlobStream;  
//char * pUSStream;  
std::shared_ptr<char> pUSStream;

std::vector<TypeDefinition> TypeDefinedList;  
std::vector<FieldDefinition> FieldDefinedList;  
std::vector<MethodDefinition> MethodDefinedList;  
std::vector<ConstantDefinition> ConstantDefinedList;  
};

class PeLoaded {  
public:  
DWORD nMagic;  
BOOL bValidateFailed;  
int ArchitectureBitsNumber; // x16/x32/x64  
UINT nFlags; // tag_PeStrFlags  
wchar_t szExtension[32];  
wchar_t *szVersion, szVersionN[32], szVersionF[128], szVersionP[128];  
wchar_t szProduct[128];  
wchar_t szCompany[128]; // ??? company, ??? copyright?  
wchar_t szInfo[512]; // ?????? ??????????  
NetRuntime netRuntime;  
//  
PBYTE pMappedFileBase;  
ULARGE_INTEGER FileSize;  
ULARGE_INTEGER FileFullSize;  
PIMAGE\_NT\_HEADERS32 pNTHeader32;  
PIMAGE\_NT\_HEADERS64 pNTHeader64;  
bool Is64Bit;  
WORD Machine;  
};

[/cce_cpp]

Se avete spunti o sonsigli sono tutti ben accetti.

ps. so che non è sicuramente il modo più semplice per imparare il c++, ma&#8230;. ho voluto unire l&#8217;utile al dilettevole 😀

pps. Paolo Manco, ho visto solo ora la tua ultima risposta: si la funzione è quella, grazie per l&#8217;indicazione. Indi se ho ben compreso, meglio non utilizzare shared_ptr ma semplici puntatori?