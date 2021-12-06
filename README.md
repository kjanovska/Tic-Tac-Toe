## Algoritmus Mini-max s alfa-beta prořezáváním
K ilustraci tohoto algoritmu jsem si vybrala hru Piškvorky. V mojí verzi se jedná o herní plochu 5x5 a hráč je vítězný, pokud má za sebou v řadě/sloupci/diagonále 4 stejné znaky.
Hraje AI proti lidskému hráči. Lidský hráč zadává při vyzvání čísla od 0 do 24 (indexy jednotlivých políček) podle toho, kam chce táhnout.
Jako první jede hráč AI se znakem 'X'. První tah se vygeneruje náhodně.
Další tah AI hráče už volá algoritmus mini-max, který jsem ovšem upravila tak, aby počítal jen do hloubky 4. Je to z důvodu, že ve větších hloubkách algoritmu trvá příliš dlouho se rozhodnout. I v hloubce 4 je několik prvních pohybů poměrně dlouhá doba, již je to však snesitelné, a tak jsem hloubku už více neomezovala.
Pokud do hloubky 4 nedojde do listu, zavolá se evaluační funkce `utility`:
- Tato funkce nejdříve zkontroluje, jestli jsou už zaplněny všechna políčka (= v poslední vrstvě došel do listu). Pokud ano, vrátí skóre podle toho , kdo vyhrál a v jaké vrstvě se tomu tak stalo (např. pokud by byl pro 'X' vítězný stav v zanoření 3, vracené skóre by bylo ```points += 1000 + 3*100 ```
- Pokud stav ve 4. vrstvě není listem, zavolá se heuristická funkce `AI.player_advantage(state, layer)`, kde `state` je stav herní plochy v daném uzlu a `layer` je vrstva/hloubka, do které se zanořil.
- funkce `AI.player_advantage(state, layer)` dále pak postupně volá pomocné funkce `row_advantage, column_advantage, diagonal_advantage`, které pomocí metody `check_sign_count` hledají, jaké jsou počty X a O pohromadě. Za 1 znak je 1 bod, za 2 znaky pohromadě 10 bodů atd.. Součet těchto čísel je pak skóre, které se z heuristické funkce vrací. Od tohoto skóre však musí být odečtena hloubka, aby si AI hráč nevybral delší cestu s mnoha slibnými výsledky před cestou která vede např. k okamžitému vítězství.

Funkce minimax rekurzivně na každého potomka hrací plochy volá funkci `max_value` (tedy případ kdy na tahu je maximizer = AI hráč), ze které se pak opět rekurzivně volá `min_value` (na tahu je minimizer = lidský hráč), a `max_value` a `min_value` se ve volání střídají (jelikož po každém tahu se mění hráč). V těchto dvou funkcích taky dochází k alfa-beta prořezávání:
- alfa a beta jsou inicializovány v minimax hodnotami -inf a inf
- `max_value`: v případě, že momentální dosažené skóre potomka je větší rovno beta, dojde k jednomu prořezání a okamžitému vrácení dané hodnoty. V opačném případě se pak alfa nastavuje jako maximum ze sebe a z hodnoty `value`
- `min_value`: probíhají operace opačné, než v `max_value`, tedy `value` se okamžitě vrátí, pokud je menší rovno alfa, a jinak se beta nastaví na minimum z beta a `value`

Tento postup se ukázal funkční do jisté míry, ale narazila jsem na problém, když algoritmus vyhodnotí několik "stejně nejlepších" možných pohybů. V tuto chvíli se vrátil pohyb na políčko s nejmenším indexem. Toto však nebyl vždy správný pohyb, jelikož tak AI hráč ignoroval situace, jako je například tato:
```
|-------------|
| || || || || |
|-------------|
|X||X||X||O|| |
|-------------|
| || ||O|| ||O|
|-------------|
| || || || || |
|-------------|
| || || || || |
|-------------|
```
V tuto chvíli by AI hráč nezabránil výhře lidského hráče tím, že by mezi dvě 'O' vložil 'X', ale táhne na první políčko, které má nejlepší výsledek, který jich ale více sdílí. Tedy místo:
```
|-------------|
| || || || || |
|-------------|
|X||X||X||O|| |
|-------------|
| || ||O||X||O|
|-------------|
| || || || || |
|-------------|
| || || || || |
|-------------|
```
provede:
```
|-------------|
| || || || || |
|-------------|
|X||X||X||O||X|
|-------------|
| || ||O|| ||O|
|-------------|
| || || || || |
|-------------|
| || || || || |
|-------------|
```
Tomuto jsem se pokusila zabránít přidáním funkce `is_best_solution(self, board, child)` přímo do funkce minimax. Pro každý možný následující tah se tedy uvažuje, zda-li se hrací plocha nenachází v jednom z 'ohrožujících' stavů, jako je například ten výše. Pokud ano, zjistí se, jestli daný potomek tuto situaci řeší. Pokud ano, provede se takový pohyb. Pokud ne, minimax pokračuje pro další potomky.
Tímto se poněkud napravilo uvažování algoritmu v takovýchto situacích a přitom jsem neovlivnila rozhodování AI hráče v situacích, které by přímo neovlivnily jeho prohru. Zároveň díky této funkci dochází k dalšímu "prořezávání", když po nalezení potomka přímo řešícího "krizovou" situaci dojde k okamžitému pohybu a nekontroluje se celý zbytek potomků. Díky tomu se pak rozhodnutí může razantně urychlit.¨

Ve funkci `minimax` jsem ponechala vypisování na obrazovku. Na něm je vidět, jaké skóre možné stavy dosáhly (větší = lepší). Číslo potomka je indexem políčka, které by mělo být v takovém tahu zaplněno.

Soubor `tic-tac-toe.py` obsahuje veškeré třídy a funkce a je spustitelný.

