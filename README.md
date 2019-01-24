# Clearer database
## Rationale
If you're an add-on developper, you may hate anki's database. It's
totally unreadable. It's hard to get a direct access in it to debug
it.

Because configuration is saved in a json string. Because fields and
tags are saved as concatenated text.

Thus, this add-on's only purpose is to help correct all of this. This
add-on create a new database, which we'll call the "readable
database". It puts in this database the content from the original anki
database which was hard to read. You can then edit the readable
database and the edition will be ported to anki's database.

## Basic usage
In this section, we describe the most basic usage of this add-on. We
assume you keep the default configurations. Each options (configurable
using the add-on manager) are explained in the next section.

### Create the readable back
In the main window, choose "create the readable tables" to obtain the
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

All tables except ```fields``` and ```tags``` have a column
called ```json```. This column contains the ```json``` of the object,
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
choose "rebuild database". The content of the readable database will
be ported to anki database. The only exception is the ```json```
column, which will be ignored.

Note that content is edited or added, but not deteled.

If the database can't be rebuild, you'll have an error
message. Hopefully, it will be clear. But you may also obtain a python
error message if it is a case I didn't think of. Please create a bug
report on github, so I could correct this case.

An example of possible error: if you have a note type with 2 fields,
but only have two fields for this note in the readable database after
you did edit it. In this case, the note can't be rebuild.

### Delete the new tables
You can destroy the new tables by clicking the button "delete the new
tables". While you keep the decks default configuration, this action
is pretty useless. It only free spaces on your disk.

### Database constraints
The tables are created with constraints which should make sens if it
was a database used in a real program. Thus, the id of each table is
unique. For example, in the table fieldnames, the pair ```(ord,
mid)``` is unique. Furthermore, ```mid``` is a reference to the table
model's column id.

Cascading in case of update/deletion is set to what makes sens to
me. In the previous example, if the ```id``` is changed in a model,
then it is chagend in the fieldname. If the model is deleted, the
fieldname of this id is also deleted.

## Configurations
### Only dealing with some tables

You can decide which table to consider using the configuration
"tables". In the dictionnary of a table, set "consider" to false if
you don't want it to be considered in any actions.


The "references constraints" are added only when it is a reference to
a table in this database. In the table fieldnames, ```mid``` is a a
reference to the table models if this table in added in the readable
database.


### Add the tables in anki's database.

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
this behavior in the configuration by setting the ```deletion``` to
true.

Note that if you delete a field name, for example, you'll obtain an
error message, unless you also deleted the associated note or edited
it's note type.

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
