# TDD
Test Driven Designing in Python 3

### Why did you end up making this

I made this tdd app during a [Coursera bioinformatics course](https://en.coursera.org/specializations/bioinformatics). You can find most (if not all) the course's problens in [Rosalind](http://rosalind.info/problems/list-view/?location=bioinformatics-textbook-track). Problem's input and output always had the same format: a string. You can ckeck this if you open a Rosalind problem and look its specification, with the *sample dataset*, *extra dataset* and *debug datasets*.

![Sample input and output.png](https://cloud.githubusercontent.com/assets/17472377/20877786/47b1f782-bacb-11e6-8469-d94cbc678c27.png)

So, as I already had all the datasets before starting programming, I could see as a **`Test Driven Development`**. I decided to fully automate the process, so I made a database with a table. Each entry has 3 fields: method name, input data and output data. I made an app that opens the database, and for each entry reads the name of the method, creates a call to that method using reflection, passes the data input as a parameter and gets its response. Then, compares the actual response with the expected output in the database.

![sample io in sqlite database.png](https://cloud.githubusercontent.com/assets/17472377/20877789/50db77e8-bacb-11e6-9aaf-99094676c7a8.png)

Well, actually it's a bit more complicated: the method is not actually called by my app. Instead, it creates a test suite using **`PyUnit`** (Python's equivalent to JUnit), and creates one test case for every method in the database. But you get the idea.

### That's enough drag. I wanna see it working!

So... Have you already tried to run it!?

![no module named foo.png](https://cloud.githubusercontent.com/assets/17472377/20877793/574d2eaa-bacb-11e6-8a8c-6b678629d421.png)

Ok, if you do so, you'll get an error saying "No module named 'foo'". That's because the app run in a module called `test_foo.py` expects to find the methods to test in `foo.py`. More generically, `test_<module>.py` looks for methods in `<module>.py`.

![No database found.png](https://cloud.githubusercontent.com/assets/17472377/20877801/60ed91a2-bacb-11e6-865a-1582ce3dea40.png)

Now an **`SQLite`** database has been created. It has the name `foo.sqlite3`, or generically `<module>.sqlite3`. It's a database with a single table. There you can add the name of the method to test, and its input and expected output. Don't worry if you haven't already written it in `<module>.py`: you can set a `0` in the `perform_test` column, or even if it is set to 1 and the method doesn't exist, a `PyUnit` pragma is used specifiying the method is not implemented yet.

So, now you can rename `test_foo.py` to your `test_<module>.py` and run it once to create the database. Then you can start adding tests into the database, and writing your methods. Run `test_<module>.py` whenever you want to pass the tests.
