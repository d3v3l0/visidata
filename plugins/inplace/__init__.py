from visidata import Column, vd, VisiData, options, ColumnExpr, CompleteExpr, fail, EscapeException, Sheet, undoAddCols


@Column.api
def updateExpr(col, val):
    col.name = val
    try:
        col.expr = val
    except SyntaxError:
        col.expr = None

    col.sheet.draw(vd.scr)


@VisiData.api
def addcol_expr(vd, sheet, colidx):
    try:
        c = sheet.addColumn(ColumnExpr("", width=options.default_width), index=colidx)
        oldidx = sheet.cursorVisibleColIndex
        sheet.cursorVisibleColIndex = sheet.visibleCols.index(c)

        expr = sheet.editCell(sheet.cursorVisibleColIndex, -1,
                                completer=CompleteExpr(sheet),
                                updater=lambda val,col=c: col.updateExpr(val))

        c.expr = expr or fail("no expr")
        c.width = None
    except (Exception, EscapeException):
        sheet.columns.remove(c)
        sheet.cursorVisibleColIndex = oldidx
        raise


Sheet.addCommand(None, 'addcol-expr', 'addcol_expr(sheet, cursorColIndex+1)', undo=undoAddCols)
