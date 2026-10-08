# computorV2

Interpréteur de calcul en ligne de commande, en Python. Rationnels, complexes,
matrices et fonctions à une variable.

## Utilisation

Python 3, aucune dépendance pour le mode console.

```sh
python3 main.py
```

```
> x = 2
2
> y = 4 * i
4i
> x + y = ?
2 + 4i
> m = [[1,2];[3,4]]
[[1, 2]; [3, 4]]
> f(z) = z^2 + 3
z^2 + 3
> f(2) = ?
7
> t^2 + 5t = 10 ?
Reduced form: t^2 + 5t - 10 = 0
Polynomial degree: 2
Discriminant (Delta): 65
Discriminant is strictly positive, the two solutions are:
-6.531129
1.531129
```

`vars` liste les variables stockées, `history` les entrées précédentes, `exit`
ou `quit` sort. Les noms de variables ne sont pas sensibles à la casse : `a` et
`A` sont la même.

Interface graphique (bonus) : `python3 main.py --gui`.

## Ce qui est géré

- types : rationnels, complexes (`i`), matrices `[[1,2];[3,4]]`, fonctions `f(x) = ...`
- opérateurs : `+ - * /`, modulo `%`, puissance entière `^`, produit matriciel `**`
- affectation et réaffectation, le type est inféré
- `?` en fin de ligne : évalue une expression (`x + y = ?`) ou résout une
  équation polynomiale jusqu'au degré 2
- multiplication implicite : `2i`, `4x`, `2(x + 1)` forment un bloc, donc `4x / 2x`
  vaut 2
- `-2^2` vaut -4 et `2^3^2` vaut 512, comme en maths
- division par une fraction passe par la couche rationnelle, pas par des floats,
  pour éviter les `(2^1/2)^2 = 1.9999999`

## Fichiers

```
main.py              shell interactif, point d'entrée
src/lexer/           tokenisation
src/parser/          analyse syntaxique
src/core/            types (rational, complex, matrix, function, polynomial) et contexte
src/utils/errors.py  erreurs math et parsing
src/gui/window.py    interface graphique
defense_tester.py    batterie de tests pour la soutenance
setupV2.sh           env conda, optionnel (`./setupV2.sh clean` pour supprimer)
```

## Tests

```sh
python3 defense_tester.py
```
