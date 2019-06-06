# Readable database
## Rationale
If you're an add-on developper, you may hate anki's database. It's
totally unreadable. It's hard to get a direct access in it to debug
it.

Because configuration is saved in a json string. Because fields and
tags are saved as concatenated text.

Thus, this add-on's only purpose is to help correct all of this. It
allow to do mostly two things.

### Reading anki database
This add-on create a new database, which we'll call the "readable
database". It puts in this database the content from the original anki
database which was hard to read. You can then edit the readable
database and the edition will be ported to anki's database.

### Creating a readable database and port it to anki.
Sometime, I want to create complex models. I prefer to create them
directly in a readable database, and then port them to anki. This
add-on allow you to do that. It creates empty tables you can fill as
you want. Once filled, you can use the add-on to port those new table
to anki's database.

**WARNING: This functionnality should be considered in BETA mode. It
is entirely possible that it breaks thing, so do a backup and check
the result if you use this functionnality. And please let me know any
problem you had. I tested the add-on but I may have forgotten some to
test some cases !**

## Basic usage
In this section, we describe the most basic usage of this add-on. We
assume you keep the default configurations. Each options (configurable
using the add-on manager) are explained in the next section.

### Create the readable back
In the main window, choose "Anki to readable" to obtain the
readable tables. Those tables are created in a database in
the add-on folder.  You'll obtain a sqlite database in the add-on
folder. If you don't know how to access this folder, open the add-on
manager, select this add-on and click on "View files".

The following tables have content which is presented as concatenation
in anki's database:
* fields. It associate to a note and a field name the content of the
  field
* tags. It associate to a note one of it's tag.
The following tables are encoded as a json string, in the col table,
of anki database.
* template (aka: card type)
* models (aka: note type)
* configurations: (aka: deck's option)
* fieldnames: each field of a model. It mostly contains the name. It
  also contains some informations you can edit by clicking on "fields"
  in any edit windows.
* decks.

All tables except `fields` and `tags` have a column
called `json`. This column contains the `json` of the object,
as in anki's database. This is not really readable, but may still be
useful.

Hopefully, the column's name will be self explanatory. Or at least
clear once you open the readable database to take a look at it. Most
names are the same than in the json's base. The only exception being
Boolean, which are encoded as Boolean and not as integer. There names
is changed so that it reflects the meaning of the truth value of the Boolean.

### Rebuild your database
Let us assume you have edit the readable database. You may want to
port those change to anki's database. To do this, in the main window,
choose "Readable to anki". Most of the contents of the readable
database will be ported to anki database. The only data from the
readable database not ported to anki's database is:
* the column name `json`.
* in the table models, the column `nb_tmpls` and `nb_fields`.

In general content is edited or added. If you delete a tag, a deck, a
model or a field from the readable database, it will not be deleted
from anki database. However, if you delete a fieldname or a template
from the readable database, it will also be deleted from anki
database. This is because those two kind of data correspond to ordered
list in which the position/order is really important.

If the database can't be rebuild, you'll have an error
message. Hopefully, it will be clear. But you may also obtain a python
error message if it is a case I didn't think of. Please create a bug
report on github, so I could correct this case.

An example of possible error: if you have a note type with 2 fields,
but only have two fields for this note in the readable database after
you did edit it. In this case, the note can't be rebuild.

If the rebuilding was done properly, the table will be dropped from
the readable database.

#### You can't rebuild __Notes and cards__
Currently, you can't rebuild anything from those tables. Sorry, but
it's kinda more complicated, and I have yet to decide how to check
whether two cards are the same. Either by cid, or by (nid, ord). And
you need to merge fields in order to make a total note.

### Empty or delete the new tables
You can destroy or deleted the new tables by clicking the button
"Delete readable tables" and "Empty readable tables". While you keep
the decks default configuration, deleting the tables is pretty
useless. It only free spaces on your disk. You can use empty table to
add contents using either another program or just a database
editor. You can then port this content into anki using the action
"Readable to anki".

### Database constraints
The tables are created with constraints which should make sens if it
was a database used in a real program. Thus, the id of each table is
unique. For example, in the table fieldnames, the pair `(ord,
mid)` is unique. Furthermore, `mid` is a reference to the table
model's column id.

Cascading in case of update/deletion is set to what makes sens to
me. In the previous example, if the `id` is changed in a model,
then it is chagend in the fieldname. If the model is deleted, the
fieldname of this id is also deleted.

## Configurations
### Only dealing with some tables

You can decide which table to consider using the configuration
"tables". In the dictionnary of a table, set "consider" to false if
you don't want it to be considered in any actions.


The "references constraints" are added only when it is a reference to
a table in this database. In the table fieldnames, `mid` is a a
reference to the table models if this table in added in the readable
database.


### Add the tables in anki's database.

__THIS OPTION IS CURRENTLY REMOVED__
By default, the the new tables are created in a new database. You can
decide to create the new tables in anki's database instead. In order
to do this, set "use anki's database" to true in the add-on's
configuration.

One of the main interest of adding the table in anki's database is
that it allows to add more constraint to the database.  A reference to
the table "notes" is added in the base only if the table is added in
anki's base. If you then alter notes' nid, for example, this
modification will propagate to the fieldnames  table thanks to the
database constraint.

### Deleting entries from the database
By default, if you did delete a line in the readable database, the
deletion won't be ported to anki database. You can choose to alter
this behavior in the configuration by setting the `deletion` to
true.

A few note related to what will happen if we delete an entry, for each
table:
* template: multiple cases should be considered:
  * if you delete every template of a model, this will have no
	effect.
  * if at least one template exists for the model, then the templates
	present will be considered to be the actual list of templates. It
	is mandatory that templates are numbered from 0 up to n-1, with n
	the number of template of the model
* fieldname: the behavior is exactly the same as for template. Note
  that the field content in each note will also disappear if the
  current add-on is used for both field and field names.
* Models: if you delete a model, all of its note, card and template
  will be deleted when you check the database.
* Deck: If you delete a deck, anki's «check database» will find card without
  deck and move them to the default deck.
* fields: if you delete this, it won't be taken into account. You
  can't actually deleted a field without deleting it's whole
  note.
* tags: the tag will disappear from the note. And that's all which
  will occur.

Let us also say a word about deletion of entry in anki's database:
* note: if you delete a note, all of it's card and it's tag will
  eventually be deleted.
* card: if the template state that the card should exists, it will be
   generated again when anki realize it is missing. However, it will
   have a new id, and every related informations will be
   reinitialized.
* col: just don't do that. You'll break anki.
* graves: ard to say what will occur if you remove an entry
* revlog: the only consequence will be to sligthly change your statistics.

### Keeping readable table after rebuilding
By setting "keep table" to true, the tables won't be deleted after you
rebuild anki database. This is dangerous if the tables are in anki database.

## Warning
### Back up
Make a backup before using it. It should not create problem, but you
never know.

### Synchronization
If you decide to add tables in anki's database DO NOT SYNCHRONIZE. The
new tables may be synchronized (at least when a full synchronization
is done). Then, if the table is downloaded on ankidroid, ankidroid
bugs. You may synchronize again once those tables are deleted by
"rebuild database" or "cancel database edition"

And even without a bug, it's a bad idea to synchronize those tables,
since they takes useless space and bandwidth.

### Card generation
This add-on do not consider card's generation at all ! It means that
you have to use «check database» in the card menu, to generate all new
cards. And you have to use «Empty cards» to delete cards which should
be deleted.

## Internal
It changes no function of anki. If you set "other database" to false,
then it adds tables to the database.

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
Support me on| [![Ko-fi](https://ko-fi.com/img/Kofi_Logo_Blue.svg)](Ko-fi.com/arthurmilchior) or [![Patreon](http://www.milchior.fr/patreon.png)](https://www.patreon.com/bePatron?u=146206)
