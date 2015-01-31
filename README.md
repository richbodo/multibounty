# multibounty
#MultiSig Bounty Library

Provides library and examples that use the bitcoin blockchain to solve the following problem:

You are an author of some code or other work on github.  You want to incentivize people to do work, such as fix bugs in code, or supply excellent edits to documentation.

**Three steps need to be made:**

1) **Bounty Transaction:** You want to offer a bounty that is irrevocable, to be awarded for the work desired, to the first person to satisfy some condition.  So you make a Bounty Transaction locking up that money for that purpose.  

2) **Decision:** A decision is made as to who should win the bounty, either by You, or by the MultiBounty Platform as Oracle.  

3) **Award Transaction:** Finally, an award must be made sending the output of the Bounty Transaction to the receiving address of the winner.

**Future Work:** Many different possibilities exist for more complex use cases and workflows.  

In the first step, the Bounty could be multiparty (many people chip in to the award, some number need to be in agreement to present it).  

In the second step, the Decision to award a bounty, can be complex, involving multiple parties, voting, test driven development, handoff of copyright, and more.  The bounty could also be restricted to a list of individuals (or even just to the author).

In the third  step, the award transaction might be given partially to many submissions that all contribute some value.  

Finally, the underlying services for blockchain manipulation (blockcypher, block.io, ethereum, etc) and decision making (github, travis.ci) could be abstracted.  We'll just start simple, though.

Two of the simplest workflows we imagine are included below in use cases 1 and 2.

![Simple Use Cases](./images/MultiBounty_Simple_UseCases.png)

MultiBounty was created as a blockchainu midterm project.


