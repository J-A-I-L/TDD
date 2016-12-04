# TDD
Test Driven Designing in Python 3

I made this tdd app during a [Coursera bioinformatics course](https://en.coursera.org/specializations/bioinformatics). You can find most (if not all) the course's problens in [Rosalind](http://rosalind.info/problems/list-view/?location=bioinformatics-textbook-track). Problem's input and output always had the same format: a string. You can ckeck this if you open a Rosalind problem and look its specification, with the *sample dataset*, *extra dataset* and *debug datasets*.


So, as I already had all the datasets before starting programming, I could see as a **Test Driven Development**. I decided to fully automate the process, so I made a database with a table. Each entry has 3 fields: method name, input data and output data. I made an app that opens the database, and for each entry reads the name of the method, creates a call to that method using reflection, passes the data input as a parameter and gets its response. Then, compares the actual response with the expected output in the database.

Well, actually it's a bit more complicated: the method is not actually called by my app. Instead, it creates a test suite using **PyUnit** (Python's equivalent to JUnit), and creates one test case for every method in the database. But you get the idea.
