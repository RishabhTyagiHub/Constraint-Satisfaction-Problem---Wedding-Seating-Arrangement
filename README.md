# Constraint-Satisfaction-Problem---Wedding-Seating-Arrangement

Problem description: You need to plan a wedding seating arrangement for n guest. Some of the pairs of guests are friends, some other are enemies and rest of them are indifferent to each other.
Friends: Friends or couple need to sit together on a table.
Enemies: Enemies hate each other and can't sit at the same table.
Indifferent: Guests who are indifferent to each other don't mind sitting at the same table or not.

The following are the contraints of this problem:
(a) Each guest should be seated at one and  only one table.
(b) For any two guests who are Friends, you should seat them at the same table.
(c) For any two guests who are Enemies, you should seat them at different tables.

Input to the program:
number of guests < M>, the number of tables < N>, and a sparse representation of the relationship matrix  R with elements  Rij = 1 ,-1 or 0 to represent whether guests  i and  j  are Friends (F), Enemies (E) or Indifferent (I).

Created a CNF sentences for the input, Implemented the PL resolution algorithm to solve identify constraint satisfying assignment for each CNF sentence if possible or not.
If the assignment is possible then used WalkSAT to determine the arrangement of guests on the wedding day.

 
