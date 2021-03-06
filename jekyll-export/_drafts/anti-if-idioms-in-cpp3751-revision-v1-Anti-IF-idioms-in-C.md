---
id: 6495
title: Anti-IF idioms in C++
date: 2016-08-05T23:35:26+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/08/05/3751-revision-v1/
permalink: /2016/08/05/3751-revision-v1/
---
<p style="text-align: justify;">
  Last November 15th I attended the <a href="http://agileday.it" target="_blank">Italian Agile Day</a> in Ancona, where Gianluca Padovani, Marco Foco, and I facilitated a workshop on refactoring in C++ (if you like, read more details <a href="http://www.italiancpp.org/2014/11/16/italy-speaks-cpp-too/#workshop" target="_blank">here</a>). Before our session, I attended a couple of talks and one was about &#8220;IF-Oriented Programming vs Object Oriented Programming&#8221;, by <a href="http://claudiopattarello.blogspot.it" target="_blank">Claudio Pattarello</a> (a former collegue of mine). I enjoyed this talk because it was completely on the code (in C#) and rich of interesting examples on removing IFs. I have attended this kind of talks for at least 8 years (the first time was at the university, in 2006) but this time something was different: each solution Claudio introduced could be written in C++ with almost no effort. This wouldn&#8217;t have been possible without new C++.
</p>

<p style="text-align: justify;">
  In this post I&#8217;d like to show you how to rewrite these idioms in C++, starting from a C# snippet. And the resulting code is pretty much identical. <a href="https://iopvsoop.codeplex.com/SourceControl/latest" target="_blank">Here are Claudio&#8217;s examples</a>. First let me clarify:
</p>

<li style="text-align: justify;">
  I&#8217;m skipping <strong>visitors</strong> because they are well-known in C++ (and from C++11, variadic templates could help even more);
</li>
<li style="text-align: justify;">
  Claudio&#8217;s target was to show different ways to remove IFs and to play with the code. The real point is: don&#8217;t tell &#8220;the IF cannot be removed&#8221;, but instead, wonder if it&#8217;s worth. For this reason, I&#8217;m not discussing edge cases nor saying these rules apply everywhere (they don&#8217;t)..
</li>
<li style="text-align: justify;">
  I&#8217;m not saying &#8220;this is the best thing you can do in C++&#8221;. For example: <a href="http://www.italiancpp.org/2014/11/23/anti-if-idioms-in-cpp/#comment-81" target="_blank">as Nicola suggested</a>, the first example I&#8217;m showing could be rewritten by using an <em>optional type</em>, that is (likely) a more effective thing to do in C++ and it results in less code. Sure, we have specific idioms in our favorite language but I think it’s lovely that we are able to reuse the same code from other languages with a little effort. And this is also appealing for other programmers who want to experience C++, maybe by starting coding idioms they know. Please, stop me if I&#8217;m raving!
</li>

Let&#8217;s start with an example you have to deal with a **null**. Here is the first version of the code:

[snippet]

<pre>public void NullResult_IF()
{
      var employeeRepository = new EmployeeRepositoryNullIF();
      var employee = employeeRepository.GetOrNull("CLAPAT01");
      if (employee!=null)
         Assert.AreEqual("Claudio", employee.Name);
}</pre>

[/snippet]

<p style="text-align: justify;">
  What if the repository does not contain the name we are looking for? It returns a null. Null case has to be handled. Suppose you have to fill a form with employee&#8217;s data. Using a <strong>NullObject</strong> doesn&#8217;t help so much because you won&#8217;t fill a form with fake values.
</p>

<p style="text-align: justify;">
  Then, the proposed solution is to add a layer of abstraction and pass an action instead of checking the null case by hand:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public interface IPerformer&lt;out T&gt;
{
    void Ask(Action&lt;T&gt; action);
}

public class Performer&lt;T&gt; : IPerformer&lt;T&gt;
{
    private readonly T value;

    public Performer(T value)
    {
        this.value = value;
    }

    public void Ask(Action&lt;T&gt; action)
    {
        action(value);
    }
}

public class NoPerformer&lt;T&gt; : IPerformer&lt;T&gt;
{
    public void Ask(Action&lt;T&gt; action) { }
}

public class EmployeeRepositoryNullNOIF
{
    //...

    public IPerformer&lt;Employee&gt; Get(string number)
    {
        var employee = repository.SingleOrDefault(e =&gt; e.Number == number);
        if (employee==null)
            return new NoPerformer&lt;Employee&gt;();
        return new Performer&lt;Employee&gt;(employee);
    }
}

public void CentralisedNullResult_NOIF()
{
    var employeeRepository = new EmployeeRepositoryNullNOIF();
    var employee = employeeRepository.Get("CLAPAT01");
    employee.Ask(e =&gt; Assert.AreEqual("Claudio", e.Name));
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  <strong>employeeRepository</strong> now returns an <strong>IPerformer<T></strong>, an interface you can ask to call a lambda which wants a parameter of type T. In this example, the lambda will be called only if the T &#8220;is valid&#8221;. An alternative consists in providing also a lambda for the failing case. But now the juicy part: what does it look like in C++? This is a possible migration:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;functional&gt;
#include &lt;iostream&gt;
#include &lt;memory&gt;
#include &lt;map&gt;
using namespace std;

template&lt;typename T&gt;
class IPerformer
{
public:
    virtual ~IPerformer() = default;
    virtual void Ask(function&lt;void(const T&)&gt; f) = 0;
};

template&lt;typename T&gt;
class NoPerformer : public IPerformer&lt;T&gt;
{
public:
    void Ask(function&lt;void(const T&)&gt;) override 
    {

    }
};

template&lt;typename T&gt;
class Performer : public IPerformer&lt;T&gt;
{
public:
    Performer(T _value)
        : value(move(_value))
    {

    }

    void Ask(function&lt;void(const T&)&gt; action) override 
    {
        action(value);
    }

private:
    T value;
};

struct Employee
{
    string Name;
    string Last;
    string Number;
};

class EmployeeRepositoryNullNOIF
{
public:
    unique_ptr&lt;IPerformer&lt;Employee&gt;&gt; Get(const string& number)
    {
        const auto it = employees.find(number);
        if (it != end(employees))
            return make_unique&lt;Performer&lt;Employee&gt;&gt;(it-&gt;second);
        return make_unique&lt;NoPerformer&lt;Employee&gt;&gt;();
    }

    map&lt;string, Employee&gt; employees = { 
        {"1", {"Marco", "Arena", "1"}},  
        {"2", {"Claudio", "Pattarello", "2"}}
    };
};

int main()
{
    EmployeeRepositoryNullNOIF repo;
    auto employee = repo.Get("2");
    employee-&gt;Ask([](const Employee& e) {
        cout &lt;&lt; e.Name &lt;&lt; " " &lt;&lt; e.Last &lt;&lt; endl;
    });
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  It&#8217;s just a toy, but you may play with this example. Ha, I forgot to say: C++ examples here are editable and runnable (thanks to <a href="http://www.stacked-crooked.com" target="_blank">Coliru</a> online compiler and <a href="http://ace.c9.io/#nav=about" target="_blank">ACE editor</a>). Then, try the code yourself!
</p>

<p style="text-align: justify;">
  C++&#8217;s control is finer, thus I considered passing T to Performer by value and then move-construct the internal one; also, T is passed to the function by const&.
</p>

Apart from these details, C++ code is pretty much the same as the C# one.

<p style="text-align: justify;">
  The next example is a variation of the previous one. It&#8217;s about doing something with the result of an operation if it succeeds, otherwise doing something else. Trivial. Here is the C# snippet:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public void ConvertNumber_IF()
{
    int number;
    if (int.TryParse("38", out number))
        Assert.AreEqual(38, number);
    else
        Assert.Fail();
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  To remove this IF, Claudio used a lambda, again:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public void ConvertNumberWrapIf_NOIF()
{
    Action action = Assert.Fail;
    ConvertNumberStatusNOIF.Parse("38", number =&gt;
    {
        action = () =&gt; Assert.AreEqual(38, number);
    });
    action();
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  As before, the lambda gets called only if the operation succeeds. C++ code is embarrassingly similar:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;sstream&gt;
#include &lt;functional&gt;

using namespace std;

class ConvertNumberStatusNOIF
{
public:
    static void Parse(const string& number, function&lt;void(int)&gt; action)
    {
        stringstream ss(number);
        char c;
        int age;
        if (ss &gt;&gt; age && !ss.get(c))
            action(age);
    }  
};

int main()
{
    function&lt;void()&gt; action = []{ cout &lt;&lt; "fail\n"; };
    ConvertNumberStatusNOIF::Parse("38", [&](int number)
    {
        action = [=]() { cout &lt;&lt; number &lt;&lt; endl; };
    });
    action();
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  A variation consists in making <em>action</em> a sort of scoped function (i.e. that will be executed when the scope ends &#8211; I saw this kind of workflow to handle DB transactions).
</p>

<p style="text-align: justify;">
  Going ahead, the following snippet handles error conditions by catching exceptions explicitly:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public void CatchExceptions_IF()
{
    var promocode = new PromocodeStatusIF();
    try
    {
        promocode.Apply("g128g7d2g");
    }
    catch (AlreadyUsedPromocodeException)
    {
        Assert.Pass("Already used");    
    }
    catch (ExpiredPromocodeException)
    {
        Assert.Pass("Expired");
    }
    catch (NotValidPromocodeException)
    {
        Assert.Pass("Not valid");
    }
    Assert.Fail("no exception");
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Try/Catch can be seen as another kind of IF, maybe more structured. To remove yet another IF, we pass actions instead and we let the promocode checker call the right one for us:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public void RemoveCatchExceptionsAndUseMessages_NOIF()
{
    var promocode = new PromocodeStatusNOIF();
    promocode
        .AlreadyUsed(() =&gt; Assert.Pass("Already used"))
        .Expired(() =&gt; Assert.Pass("Expired"))
        .NotValid(() =&gt; Assert.Pass("Not valid"))
        .Apply("g128g7d2g");

    Assert.Fail("no exception");
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  <strong>PromocodeStatusNOIF</strong> just calls the right action. No exceptions are involved, no manual handling to do, adding/removing logic is trivial. What does it look like in C++? Not so different:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;functional&gt;
#include &lt;string&gt;

using namespace std;

class PromocodeStatusNOIF
{
    function&lt;void()&gt; alreadyUsed = []{};
    function&lt;void()&gt; expired = []{};
    function&lt;void()&gt; notValid =  []{};

public:
    PromocodeStatusNOIF& AlreadyUsed(function&lt;void()&gt; action)
    {
        alreadyUsed = action;
        return *this;
    }

    PromocodeStatusNOIF& Expired(function&lt;void()&gt; action)
    {
        expired = action;
        return *this;
    }

    PromocodeStatusNOIF& NotValid(function&lt;void()&gt; action)
    {
        notValid = action;
        return *this;
    }

    void Apply(const string& promocode)
    {
        // logic...
        expired(); 
    }
};

int main()
{
    PromocodeStatusNOIF{}
        .AlreadyUsed([] { cout &lt;&lt; "Already used\n"; })
        .Expired([] { cout &lt;&lt; "Expired\n"; })
        .NotValid([] { cout &lt;&lt; "NotValid\n"; })
        .Apply("g128g7d2g");
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  I don&#8217;t have the final Assert.Fail because we are not really testing anything. A variation is to add the &#8220;no exception&#8221; action either in the constructor or as another function of the chain.
</p>

<p style="text-align: justify;">
  <span style="line-height: 1.5em;">The last example I show you is a singleton factory which the first time you ask an instace it creates and returns a fresh one, other times this instance is reused. The IF solution is straightforward:</span>
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public class FooSingletonLazyFactoryIF
{
    private Foo foo;

    public Foo Get()
    {
        if (foo==null)
            foo = new Foo();
        return foo;
    }
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Removing the IF is a good exercise of self-modifying lambdas:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>public class FooSingletonLazyFactoryNOIF 
{
    public FooSingletonLazyFactoryNOIF()
    {
        Get = () =&gt;
        {
            var foo = new Foo();
            Get = () =&gt; foo;
            return Get();
        };
    }

    public Func&lt;Foo&gt; Get { get; private set; }
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Forget using a local static variable, just enjoy a different way to code. What does it look like in C++? This is a possible implementation:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;functional&gt;
#include &lt;iostream&gt;

using namespace std;

struct Foo
{ 
    Foo(int _magic) 
       : magic(_magic)
    { cout &lt;&lt; "new Foo" &lt;&lt; endl; }
    int magic = 0; 
};

class FooSingletonLazyFactoryNOIF 
{
public:
    FooSingletonLazyFactoryNOIF()
    {
        _Get = [this] 
        {
            _Get = [foo=Foo{256}]() -&gt; const Foo& { return foo; };
            return _Get();
        };
    }

    const Foo& Get() const
    {
        return _Get();
    }

private:
    function&lt;const Foo&()&gt; _Get;
};

int main()
{
    FooSingletonLazyFactoryNOIF factory;
    auto&& foo = factory.Get();
    auto&& foo2 = factory.Get();
    cout&lt;&lt; foo.magic &lt;&lt; endl;
    cout&lt;&lt; foo2.magic &lt;&lt; endl;
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Thanks to init-lambda capture I was able to initialize Foo directly in the lambda. This version has a problem: what if the factory goes out of scope? The internal foo is destroyed and we have a dangling reference. Ok, you can make the factory a global object but there is another solution using smart pointers. Don&#8217;t try to move-capture a <strong>unique_ptr</strong> into the lambda because it is <strong>not</strong> possible to construct a std::function from a <strong>move-only type </strong>(cfr. §20.9.11.2.1 [func.wrap.func.con]). We can use a shared_ptr and return it, or return just a Foo*, or a weak_ptr. For example:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;functional&gt;
#include &lt;memory&gt;
#include &lt;iostream&gt;

using namespace std;

struct Foo
{ 
    Foo(int _magic) 
       : magic(_magic)
    { cout &lt;&lt; "new Foo" &lt;&lt; endl; }
    int magic = 0; 
};

class FooSingletonLazyFactoryNOIF 
{
public:
    FooSingletonLazyFactoryNOIF()
    {
        _Get = [this] 
        {
            auto foo = make_shared&lt;Foo&gt;(256);
            _Get = [foo=move(foo)]() { return foo; };
            return _Get();
        };
    }

    auto Get() const
    {
        return _Get();
    }

private:
    function&lt;weak_ptr&lt;Foo&gt;()&gt; _Get;
};

int main()
{
    FooSingletonLazyFactoryNOIF factory;
    auto foo = factory.Get();
    if (auto spt = foo.lock()) // not needed actually
    {
        cout &lt;&lt; spt-&gt;magic &lt;&lt; endl;
    }
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  As you can note, C++ snippets are very similar to C# ones. Since C++ gives more control and it doesn&#8217;t have a garbage collector, you need to be careful of more aspects. In particular, dealing with self-modifying lambdas could lead to several problems like capturing local variables by reference.
</p>

<p style="text-align: justify;">
  Using std::function is not optimal. Not only because of its runtime cost but also because of its inability to work with move-only captured types. I&#8217;d like also to share a fact you could care about when dealing with self-modifying lambdas. Suppose you wrote this circular object pool by using the same ideas we discussed a moment ago:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>class Pool
{
    function&lt;int()&gt; generator;

    function&lt;int()&gt; next(vector&lt;int&gt; v, size_t i)
    {
        return [this, v=move(v), i]{
            auto tmp = v[i];
            auto size = v.size();
            generator = next(move(v), (i+1)%size);
            return tmp;
        };
    }
public:    
    Pool(vector&lt;int&gt; v)
        : generator {next(move(v), 0)}
    {

    }

    int operator()()
    {
        return generator();
    }
};

//...user code
Pool pool { {1,2,3} };
cout &lt;&lt; pool.Get() &lt;&lt; endl; // 1
cout &lt;&lt; pool.Get() &lt;&lt; endl; // 2
cout &lt;&lt; pool.Get() &lt;&lt; endl; // 3
cout &lt;&lt; pool.Get() &lt;&lt; endl; // 1</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  You are storing the vector inside generator (which is a std::function). How many copies of this vector do you expect? You could say: &#8220;Zero! Just moves, because I&#8217;m always moving the vector from a lambda to the next one&#8221;. I thought so too. Look more carefully how you are updating the next function:  when you capture the vector by move it gets moved into the lambda. Ok. What next? You store tmp and size, ok. Then? You update generator&#8230; Ah! Moving the vector here is just a copy! Why? Because the lambda is not <strong>mutable</strong>, thus the vector is <strong>const</strong> and moving a const object is actually (and silently) a copy. I prepared this snippet to let you play (i.e. remove mutable):
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;memory&gt;
#include &lt;vector&gt;
#include &lt;functional&gt;
using namespace std;

struct sentinel
{
    sentinel() = default;
    sentinel(const sentinel&) { cout &lt;&lt; "copy" &lt;&lt; endl; }
    sentinel(sentinel&&) { cout &lt;&lt; "move" &lt;&lt; endl; }
};

class Pool
{
    function&lt;int()&gt; generator;

    function&lt;int()&gt; next(vector&lt;int&gt; v, sentinel s, size_t i)
    {
        return [this, v=move(v), i, s=move(s)]()mutable{
            auto tmp = v[i];
            auto size = v.size();
            generator = next(move(v), move(s), (i+1)%size);
            return tmp;
        };
    }
public:    
    Pool(vector&lt;int&gt; v)
       : generator {next(move(v), sentinel{}, 0)}
    {

    }

    int operator()()
    {
        return generator();
    }
};

int main()
{
    Pool p { {1,2,3} };
    cout &lt;&lt; p() &lt;&lt; endl;
    cout &lt;&lt; p() &lt;&lt; endl;
    cout &lt;&lt; p() &lt;&lt; endl;
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Target of this post was purely to implement Claudio&#8217;s examples in C++, taking into account some particularities of our favourite language. As I said, I&#8217;m not discussing edge cases nor saying these idioms apply everywhere (they don&#8217;t). If you have more examples please share them here!
</p>