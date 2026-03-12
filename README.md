# DATAFILES

A datafile have the followed structure:

```html
<sep> <label_1> <label_2> ...
obj_label1<sep>obj_label2<sep>...
```

As an example:

```c
 | nome capitulo status
Catastrophic Necromancer|111|dropado
```

The sep should be a string with no revelant whitspaces at start and end, it is:

```md
< asdf >  X
<asdf>    √
<,>       √
<|>       √
```
Be carefull with `<,>` bacause there is names that use this caracther `,`.

The labels should be a sigle world that describes the camp of the bojects. In this current version it should be [nome, capitulo, status].
