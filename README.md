# Clearer database
## Rationale
If you're an add-on developper, you may hate anki's database. It's
totally unreadable. It's hard to get a direct access in it to debug
it.

Because configuration is saved in a json string. Because fields and
tags are saved as concatenated text.

Thus, this add-on's only purpose is to help correct all of this. This
add-on extract a readable database from anki database. So you can read
easily, debug, and get all informations you need. Better yet, you can
edit this clear database. Then, using this add-on, the edition will be
sent back to the usual database anki use. (This option is not yet
developped, but it will arrive one day.)

## Usage
In the main window, choose either "clarify database" to obtain this
beautiful usable database. Or choose "rebuild database" in order to
port your change from the clear database to anki database.

## Warning
Make a backup before using it. It should not create problem, but you
never know.


## Internal
It changes no function of anki.

## Version 2.0
none

## TODO
See intro

Allow user to generate a single table and no the whole database

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-better-database
Addon number| [1585491271](https://ankiweb.net/shared/info/1585491271)
