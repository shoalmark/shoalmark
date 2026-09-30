# Anforderungen — ein Text für Entwicklung und Test

## Warum

Entwicklung und Test arbeiten von einer gemeinsamen Grundlage aus: den Anforderungen, im Repository, neben dem Code.
Die Testenden prüfen die Anforderung als Vertrag — nach dem, was sie sagt, nicht nach dem, was die Umsetzung zufällig
tut —, denn ein Testplan, der aus dem Code geschrieben wird, bestätigt nur den Code, und ein Plan außerhalb des
Repositorys läuft auseinander.

## Eine Zeile, eine Anforderung

| id | shall | source | accept |
|---|---|---|---|
| REQ-PWR-007 | Das Gerät geht 2 s nach der letzten Eingabe in den Ruhezustand. | die Produktleitung | Eingabe endet: Ruhe in < 2 s |

Die Zeilenform — die vier Spalten und was jede enthält — steht einmal, in
[`requirements/README.md`](https://github.com/shoalmark/shoalmark/blob/main/requirements/README.md) (englisch).
Diese Seite wiederholt sie nicht.

## Ihr Teil

Eine Anforderung ändert sich nur durch Ihre signierte Antwort über die Tafel — nie durch die Änderung eines Sitzes. Die
Id bleibt, die Zeile ändert sich, Git bewahrt den Verlauf. Findet ein Sitz eine Zeile falsch, stellt er eine Frage an
Sie. *Nicht anwendbar* ist eine signierte Antwort mit ihrer Begründung, nie die eines Sitzes.

## Eine regulatorische Anforderung

Nennen Sie die Klausel — Norm, Ausgabe, Klauselnummer — und schreiben Sie das eigene *shall* des Unternehmens, das sich
aus ihr ableitet. Den Text einer Norm nie ins Repository kopieren. Nie schreiben, das Projekt erfülle sie: eine
erfüllte Anforderung ist ein bestandener Test, nicht mehr.

## Wie der Nachweis sie nennt

Ein Arbeitspaket nennt, was es erfüllt, in einer Zeile seines Textes: `Satisfies: REQ-PWR-007`. Ein Test nennt die Id in
seinem Namen oder seiner Beschreibung. Das Arbeitspaket verweist auf die Id, statt das Verhalten neu zu schreiben — so
gibt es von der Anforderung nie eine dritte Fassung. Die Abnahmekriterien stehen in der Spalte `accept`.

## Noch nicht gebaut

Jedes ist eine Frage an Sie und beginnt erst mit Ihrem Wort.

- **Stufe 1**, nach der Erprobung und einem weiteren Interessenten: Prüfung von Abdeckung und Verweisen; Markierung
  dessen, was eine Anforderung nennt, sobald sie sich ändert; `--trace REQ-<id>`; eine Rückverfolgbarkeitsmatrix je
  Release, aus Git erzeugt.
- **Stufe 2:** ein Testsitz, der die Anforderungen liest und nicht die Umsetzung.
