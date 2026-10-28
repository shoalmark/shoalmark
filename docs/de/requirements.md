# Anforderungen — ein Text für Entwicklung und Test

## Warum

Entwicklung und Test arbeiten von einer gemeinsamen Grundlage aus: den Anforderungen, im Repository, neben dem Code.
Die Testenden prüfen die Anforderung als Vertrag — nach dem, was sie sagt, nicht nach dem, was die Umsetzung zufällig
tut —, denn ein Testplan, der aus dem Code geschrieben wird, bestätigt nur den Code, und ein Plan außerhalb des
Repositorys entfernt sich mit der Zeit vom Code.

## Eine Zeile, eine Anforderung

| id | shall | source | accept |
|---|---|---|---|
| REQ-PWR-007 | Das Gerät muss spätestens 2 s nach der letzten Eingabe in den Ruhezustand wechseln. | die Produktleitung | Eingabe endet: im Ruhezustand nach < 2 s |

Die Zeilenform — die vier Spalten und was jede enthält — steht einmal, in
[`requirements/README.md`](https://github.com/shoalmark/shoalmark/blob/main/requirements/README.md) (englisch).
Diese Seite wiederholt sie nicht.

## Dein Teil

Eine Anforderung ändert sich nur durch deine signierte Antwort über das Board — nie durch die Änderung einer Rolle. Die
Id bleibt, die Zeile ändert sich, Git bewahrt den Verlauf. Findet ein Agent eine Zeile falsch, stellt er dir eine
Frage. *Nicht anwendbar* ist eine signierte Antwort mit ihrer Begründung, nie die einer Rolle.

## Eine regulatorische Anforderung

Nenne die Fundstelle — Norm, Ausgabe, Abschnitt — und leite daraus die eigene Pflicht des Unternehmens ab,
als Satz in der Spalte `shall`. Den Text einer Norm nie ins Repository kopieren. Nie schreiben, das Projekt erfülle die
Norm: eine erfüllte Anforderung ist ein bestandener Test, nicht mehr.

## Wie der Beleg sie nennt

Ein Arbeitspaket nennt, was es erfüllt, in einer Zeile seines Textes: `Satisfies: REQ-PWR-007`. Ein Test nennt die Id in
seinem Namen oder seiner Beschreibung. Das Arbeitspaket verweist auf die Id, statt das Verhalten neu zu schreiben — so
gibt es von der Anforderung nie eine dritte Fassung. Die Abnahmekriterien stehen in der Spalte `accept`.

## Noch nicht gebaut

Jede Stufe ist eine Frage an dich und beginnt erst mit deinem Wort.

- **Stufe 1**, nach der Erprobung und einem weiteren Interessenten: Prüfung von Abdeckung und Verweisen; was eine
  Anforderung nennt, wird als veraltet markiert, sobald sie sich ändert; `--trace REQ-<id>`; eine
  Rückverfolgbarkeitsmatrix je Release, aus Git erzeugt.
- **Stufe 2:** eine Testrolle, die die Anforderungen liest und nicht die Umsetzung.
