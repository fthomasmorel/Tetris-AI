# Tetris-AI

## Tetris Game

We develop an AI for the Tetris Game. We fork the python Tetris from here: https://gist.github.com/silvasur/565419/7e044a90eb97eb67d600b2fb776000ba36f6fcc9. Our AI is inspired by this one: http://leeyiyuan.github.io/tetrisai/.

We develop our own AI and plug it into the python Tetris.

## Genetic Algorithm

We trained our AI using Genetic Algorithm and the Cross Entropy method. All of it is written in the ```genetic.py``` file that will train population. The logs of our different training are available in the ```logs``` folder.

```logs_v5.txt``` contains the logs of our lastest train using a limit of 500 pieces per game. We trained those population during about 4 days.

```logs_v6.txt``` contains the logs of our lastest train using a limit of 1000 pieces per game. We trained it non-stop during 2 weeks...

In those two files, each line representing an individual is formated as following:

```
[score, [list of weights for each of the 34 heuristics]]

Ex:
[399000, [-2.100689734519437, -6.296337703002559, -3.6053570383018902, -5.174030015302046, -7.094388505722243, -7.163019117701906, -4.155623378939865, -7.470271464077066, -6.837060809015177, 4.055711464398931, -23.189118507055124, -17.22774140164603, -6.636151504678342, 3.169793808221626, -18.464118325281074, -3.892389642098916, -6.496728529483608, -9.168122545328442, -3.8031204486650156, -1.1073865709954989, -13.649143804127453, -4.615274667006191, 1.1085085503624723, -3.115040621666638, -6.324824019458616, -6.621636476173672, -3.356875697348909, -4.568217955358195, -7.329346044325321, -1.8518026355838344, 9.84688820557799, -8.194108483773855, -9.07005038806947, 3.149233388252534]]
```

The score is computed using the following formula :

```
nb_line_completed*1000 + nb_piece_dropped
```
