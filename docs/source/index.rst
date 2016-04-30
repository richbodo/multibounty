Multibounty - A bounty site experiment using bitcoin multisig
=============================================================

Summary 
=======

We used meteor and the Block.io API to demonstrate multisig BTC transactions on a bounty site.

Although the site worked, our hope was that we could maintain a trustless environment.  That was found to be impossible.

We found that the wallets of all users that are party to a transaction must support all features of that transaction, or the unsupported features (and the transaction) are not trustable.

Blockchains like ethereum may someday require clients to support features like multi-sig by definition, which would make those features as trustworthy as the blockchain itself.

This was a midterm project for Blockchain University.  We put together a small `presentation here <https://github.com/richbodo/multibounty/blob/master/presentation/mb_presentation.pdf>`_.

Contents:
^^^^^^^^^

.. toctree::
   :maxdepth: 2

   LICENSE
   HELP


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

