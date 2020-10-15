---
id: 9224
title: Trucchi template
date: 2019-10-11T11:10:01+02:00
author: marco
layout: revision
guid: https://www.italiancpp.org/2019/10/11/9223-revision-v1/
permalink: /2019/10/11/9223-revision-v1/
---
using IVisitor = VisitorGenerator < double, std::string, GDCVector, GDCMatrix, GDCHypermatrix, GDCHypermatrix4D>;

class TypeErased  
{  
struct Base  
{  
virtual ~Base() = default;  
virtual void Accept(IVisitor&) const = 0;  
virtual Base* Clone() const = 0;  
};

template<typename T>  
struct Erased : Base  
{  
Erased(T val)  
: _val(std::move(val))  
{

}

Erased* Clone() const  
{  
return new Erased(*this);  
}

void Accept(IVisitor& v) const override  
{  
v.Visit(_val);  
}

private:  
Erased(const Erased&) = default;  
Erased& operator=(const Erased&) = default;

Erased(Erased&& o)  
: \_val(std::move(o.\_val))  
{

}

Erased& operator=(Erased&& o)  
{  
\_val = std::move(o.\_val);  
return *this;  
}

T _val;  
};

public:  
TypeErased() = default;

template<typename T>  
TypeErased(T val)  
: ptr(std::make_unique<Erased<T>>(std::move(val)))  
{

}

TypeErased(TypeErased&& other);  
TypeErased& operator=(TypeErased&& other);

TypeErased(const TypeErased& other);  
TypeErased& operator=(const TypeErased& other);

void Accept(IVisitor& v) const;

private:  
std::unique_ptr<Base> ptr;  
};

//

#include &#8220;TypeErased.h&#8221;

TypeErased& TypeErased::operator=(TypeErased&& other)  
{  
ptr = move(other.ptr);  
return *this;  
}

TypeErased::TypeErased(TypeErased&& other)  
: ptr(move(other.ptr))  
{

}

TypeErased::TypeErased(const TypeErased& other)  
: ptr(other.ptr->Clone())  
{

}

TypeErased& TypeErased::operator=(const TypeErased& other)  
{  
ptr.reset(other.ptr->Clone());  
return *this;  
}

void TypeErased::Accept(IVisitor& v) const  
{  
return ptr->Accept(v);  
}

//

template<typename T>  
struct VisitorFunctionGenerator  
{  
virtual void VisitImpl(const T&) = 0;  
};

template<typename&#8230; T>  
struct VisitorGenerator : VisitorFunctionGenerator<T>&#8230;  
{  
virtual ~VisitorGenerator() = default;

template<typename KK>  
void Visit(const KK& val)  
{  
static_cast<VisitorFunctionGenerator<KK>*>(this)->VisitImpl(val);  
}  
};