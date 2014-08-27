Python splay tree
=================

Splay tree implemented in Python with the following dictionary interface:
* insert()
* find()
* remove()

The tree is encapsulated into a single file with a single class. There are no
external dependencies.

Tests
=====

Big, slow, unit testing suites test:
* interface correctness
* internal correctness
* the correctness of the underlying binary tree with splay() mocked out

Tests are probabilistic; multiple runs reduce the chance of false positives.
