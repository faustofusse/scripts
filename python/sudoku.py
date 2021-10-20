from random import randint

VACIO = 0

ALTO_TABLERO = 9
ANCHO_TABLERO = 9

ALTO_CUADRANTE = 3
ANCHO_CUADRANTE = 3

BLUE = '\033[94m'
NATIVE = '\033[m'
LETRAS = 'abcdefghi'

def crear_juego(representacion):
    '''
    Dada una representación en cadena de un juego de Sudoku,
    devuelve un juego de Sudoku.

    El juego de Sudoku se representa como una matriz de 9x9
    donde cada elemento es un número entero o la constante
    VACIO para indicar que no se escribió ningún número en 
    esa posición.

    La representación es una cadena con el siguiente formato:

    003020600
    900305001
    001806400
    008102900
    700000008
    006708200
    002609500
    800203009
    005010300

    Donde un 0 significa que la casilla está vacía.
    '''
    filas = representacion.split("\n")
    sudoku = []
    for fila in filas:
        fila_separada = []
        for numero in fila:
            fila_separada.append(int(numero))
        sudoku.append(fila_separada)
    return sudoku

def hay_valor_en_fila(sudoku, fila, valor):
    '''
    Devuelve True si ya hay un casillero con el valor
    'valor' en la fila 'fila'.

    Por ejemplo para fila = 3 deberán revisar todas las
    siguientes celdas:
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)
    '''
    
    for numero in sudoku[fila]:
        if numero == valor:
            return True
    return False

def hay_valor_en_columna(sudoku, columna, valor):
    '''
    Devuelve True si ya hay un casillero con el valor 'valor'
    en la columna 'columna'.

    Por ejemplo para columna = 3 deberán revisar todas las
    siguientes celdas:
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3)
    '''
    for fila in sudoku:
        if fila[columna] == valor:
            return True
    return False

def obtener_origen_region(fila, columna):
    '''
    Devuelve la posición de la celda de la esquina superior izquierda
    de la región en que se encuentra la celda en (fila, columna).

    Las regiones se agrupan de la siguiente forma:
   *[0,0] [0,1] [0,2] *[0,3] [0,4] [0,5] *[0,6] [0,7] [0,8]
    [1,0] [1,1] [1,2]  [1,3] [1,4] [1,5]  [1,6] [1,7] [1,8]
    [2,0] [2,1] [2,2]  [2,3] [2,4] [2,5]  [2,6] [2,7] [2,8]

   *[3,0] [3,1] [3,2] *[3,3] [3,4] [3,5] *[3,6] [3,7] [3,8]
    [4,0] [4,1] [4,2]  [4,3] [4,4] [4,5]  [4,6] [4,7] [4,8]
    [5,0] [5,1] [5,2]  [5,3] [5,4] [5,5]  [5,6] [5,7] [5,8]

   *[6,0] [6,1] [6,2] *[6,3] [6,4] [6,5] *[6,6] [6,7] [6,8]
    [7,0] [7,1] [7,2]  [7,3] [7,4] [7,5]  [7,6] [7,7] [7,8]
    [8,0] [8,1] [8,2]  [8,3] [8,4] [8,5]  [8,6] [8,7] [8,8]

    Las celdas marcadas con un (*) son las celdas que deberá 
    devolver esta función para la correspondiente región.

    Por ejemplo, para la posición (fila = 1, columna = 4) la función
    deberá devolver (0, 3).
    '''
    nuevaFila = 0
    nuevaColumna = 0
    if fila <= 2:
        nuevaFila = 0
    elif 5 >= fila >= 3:
        nuevaFila = 3
    else:
        nuevaFila = 6
    if columna <= 2:
        nuevaColumna = 0
    elif 5 >= columna >= 3:
        nuevaColumna = 3
    else:
        nuevaColumna = 6
    return nuevaFila, nuevaColumna

def hay_valor_en_region(sudoku, fila, columna, valor):
    '''
    Devuelve True si hay hay algún casillero con el valor `valor`
    en la región de 3x3 a la que corresponde la posición (fila, columna).

    Ver como se agrupan las regiones en la documentación de la función
    obtener_origen_region.
    
    Por ejemplo, para la posición (fila = 0, columna = 1) deberán revisar 
    si está `valor` en todas las siguientes celdas:
    (0, 0), (0, 1) (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2).
    '''
    filaRegion, columnaRegion = obtener_origen_region(fila, columna) 
    for fila in sudoku[filaRegion:filaRegion+3]:
        for numero in fila[columnaRegion:columnaRegion+3]:
            if numero == valor:
                return True
    return False

def es_movimiento_valido(sudoku, fila, columna, valor):
    '''
    Devuelve True si se puede poner 'valor' en la posición
    (fila, columna) y el Sudoku sigue siendo válido; o False
    en caso contrario.

    'valor' se puede ubicar en la posición (fila, columna) si
    se cumple lo siguiente:
     - Ningún otro elemento que esté en la misma fila es igual a 'valor'
     - Ningún otro elemento que esté en la misma columna es igual a 'valor'
     - Ningún otro elemento que esté en la misma región es igual a 'valor'
    
    No modifica el Sudoku recibido.
    '''
    movimiento_invalido = hay_valor_en_columna(sudoku, columna, valor) or hay_valor_en_fila(sudoku, fila, valor) or hay_valor_en_region(sudoku, fila, columna, valor)
    return not movimiento_invalido

def insertar_valor(sudoku, fila, columna, valor):
    '''
    Intenta insertar el valor de la celda en la posición 
    (fila, columna). 
    
    Si el movimiento es válido se devolverá un nuevo Sudoku
    con el valor cambiado. En caso contrario se devolverá el
    mismo Sudoku que se recibió por parámetro.
    '''
    nuevoSudoku = []
    for i in sudoku:
        nuevoSudoku.append(i.copy())
    if es_movimiento_valido(nuevoSudoku, fila, columna, valor): 
        nuevoSudoku[fila][columna] = valor
    return nuevoSudoku

def borrar_valor(sudoku, fila, columna):
    '''
    Borra el valor de la celda que está en la posición
    (fila, columna).

    No modifica el Sudoku recibido por parámetro, devuelve uno
    nuevo con la modificación realizada.
    '''
    nuevoSudoku = []
    for i in sudoku:
        nuevoSudoku.append(i.copy())
    nuevoSudoku[fila][columna] = VACIO
    return nuevoSudoku

def esta_terminado(sudoku):
    '''
    Devuelve True si el Sudoku está completado 
    correctamente.

    Un Sudoku está completado correctamente cuando todas 
    sus celdas tienen números y todos los números son válidos
    (es decir, no hay repetidos en la columna, ni en la fila
    ni en la región).
    '''
    for i in range(ALTO_TABLERO):
        fila = sudoku[i]
        for j in range(ANCHO_TABLERO):
            numero = fila[j]
            if numero == VACIO or not es_movimiento_valido(borrar_valor(sudoku, i, j), i, j, numero):
                return False
    return True

def obtener_valor(sudoku, fila, columna):
    '''
    Devuelve el número que se encuentra en la celda (fila, columna)
    o la constante VACIO si no hay ningún número en dicha celda.
    '''
    valor = sudoku[fila][columna]
    return valor

def hay_movimientos_posibles(sudoku):
    '''
    Devuelve True si hay al menos un movimiento posible
    en el estado actual del juego.

    Que exista un movimiento posible no implica que el juego
    pueda completarse correctamente, sólamente indica que hay
    al menos una posible inserción.
    '''
    for fila in sudoku:
        for columna in fila:
            if columna == VACIO:
                return True
    return False


# INTERFAZ

def interfaz (sudoku, numeros_insertados):
    print("    1 2 3   4 5 6   7 8 9 ")
    print('   ----------------------- ')
    for j in range(ALTO_TABLERO):
        fila = sudoku[j]
        if j == 3 or j == 6:
            print('  | - - -   - - -   - - - |')
        print(f'{LETRAS[j]} |', end= " ")
        for i in range(ANCHO_TABLERO):
            color = BLUE if ((j, i) in numeros_insertados) else NATIVE
            print((color + str(fila[i])) if fila[i] != VACIO else ' ', end= " ")
            if i in [2,5,8]:
                print(NATIVE + '|', end= " ")
        print(f'{LETRAS[j]}')
    print('   ----------------------- ')
    print("    1 2 3   4 5 6   7 8 9 ")

def jugar(sudoku_string):
    sudoku = crear_juego(sudoku_string)
    numeros_insertados = []
    while not esta_terminado(sudoku):
        interfaz(sudoku, numeros_insertados)
        movimiento = input('Ingrese movimiento [f,c,v | Si desea salir escriba "me rindo"]: ')
        if movimiento == "":
            print("Ingresa algo por lo menos...")
            continue
        if movimiento == 'me rindo': 
            break
        if movimiento[0] not in LETRAS:
            print("Acordate que la fila es una letra.")
            continue
        if len(movimiento) != 5: 
            print("Dale...Ingresa bien los datos.")
            continue
        fila = LETRAS.index(movimiento[0])
        columna = int(movimiento[2]) - 1
        valor = int(movimiento[4])
        if valor == VACIO:
            if (fila, columna) in numeros_insertados:
                sudoku = borrar_valor(sudoku, fila, columna)
                numeros_insertados.remove((fila, columna))
            else: 
                print("No podes borrar un numero del sudoku, no flashees.")
        elif es_movimiento_valido(sudoku, fila, columna, valor):
            sudoku = insertar_valor(sudoku, fila, columna, valor)
            numeros_insertados.append((fila, columna))
        else:
            print('Movimiento invalido!')
    print('GANASTE!' if esta_terminado(sudoku) else 'SALISTE PICHON') 

MAPAS = [
"""003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300""",
"""200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003""",
"""000000907
000420180
000705026
100904000
050000040
000507009
920108000
034059000
507000000""",
"""030050040
008010500
460000012
070502080
000603000
040109030
250000098
001020600
080060020""",
"""020810740
700003100
090002805
009040087
400208003
160030200
302700060
005600008
076051090""",
"""100920000
524010000
000000070
050008102
000000000
402700090
060000000
000030945
000071006""",
"""043080250
600000000
000001094
900004070
000608000
010200003
820500000
000000005
034090710""",
"""480006902
002008001
900370060
840010200
003704100
001060049
020085007
700900600
609200018""",
"""000900002
050123400
030000160
908000000
070000090
000000205
091000050
007439020
400007000""",
"""001900003
900700160
030005007
050000009
004302600
200000070
600100030
042007006
500006800""",
"""000125400
008400000
420800000
030000095
060902010
510000060
000003049
000007200
001298000""",
"""062340750
100005600
570000040
000094800
400000006
005830000
030000091
006400007
059083260""",
"""300000000
005009000
200504000
020000700
160000058
704310600
000890100
000067080
000005437""",
"""630000000
000500008
005674000
000020000
003401020
000000345
000007004
080300902
947100080""",
"""000020040
008035000
000070602
031046970
200000000
000501203
049000730
000000010
800004000""",
"""361025900
080960010
400000057
008000471
000603000
259000800
740000005
020018060
005470329""",
"""050807020
600010090
702540006
070020301
504000908
103080070
900076205
060090003
080103040""",
"""080005000
000003457
000070809
060400903
007010500
408007020
901020000
842300000
000100080""",
"""003502900
000040000
106000305
900251008
070408030
800763001
308000104
000020000
005104800""",
"""000000000
009805100
051907420
290401065
000000000
140508093
026709580
005103600
000000000""",
"""020030090
000907000
900208005
004806500
607000208
003102900
800605007
000309000
030020050""",
"""005000006
070009020
000500107
804150000
000803000
000092805
907006000
030400010
200000600""",
"""040000050
001943600
009000300
600050002
103000506
800020007
005000200
002436700
030000040""",
"""004000000
000030002
390700080
400009001
209801307
600200008
010008053
900040000
000000800""",
"""360020089
000361000
000000000
803000602
400603007
607000108
000000000
000418000
970030014""",
"""500400060
009000800
640020000
000001008
208000501
700500000
000090084
003000600
060003002""",
"""007256400
400000005
010030060
000508000
008060200
000107000
030070090
200000004
006312700""",
"""000000000
079050180
800000007
007306800
450708096
003502700
700000005
016030420
000000000""",
"""030000080
009000500
007509200
700105008
020090030
900402001
004207100
002000800
070000090""",
"""200170603
050000100
000006079
000040700
000801000
009050000
310400000
005000060
906037002""",
"""000000080
800701040
040020030
374000900
000030000
005000321
010060050
050802006
080000000""",
"""000000085
000210009
960080100
500800016
000000000
890006007
009070052
300054000
480000000""",
"""608070502
050608070
002000300
500090006
040302050
800050003
005000200
010704090
409060701""",
"""050010040
107000602
000905000
208030501
040070020
901080406
000401000
304000709
020060010""",
"""053000790
009753400
100000002
090080010
000907000
080030070
500000003
007641200
061000940""",
"""006080300
049070250
000405000
600317004
007000800
100826009
000702000
075040190
003090600""",
"""005080700
700204005
320000084
060105040
008000500
070803010
450000091
600508007
003010600""",
"""000900800
128006400
070800060
800430007
500000009
600079008
090004010
003600284
001007000""",
"""000080000
270000054
095000810
009806400
020403060
006905100
017000620
460000038
000090000""",
"""000602000
400050001
085010620
038206710
000000000
019407350
026040530
900020007
000809000""",
"""000900002
050123400
030000160
908000000
070000090
000000205
091000050
007439020
400007000""",
"""380000000
000400785
009020300
060090000
800302009
000040070
001070500
495006000
000000092""",
"""000158000
002060800
030000040
027030510
000000000
046080790
050000080
004070100
000325000""",
"""010500200
900001000
002008030
500030007
008000500
600080004
040100700
000700006
003004050""",
"""080000040
000469000
400000007
005904600
070608030
008502100
900000005
000781000
060000010""",
"""904200007
010000000
000706500
000800090
020904060
040002000
001607000
000000030
300005702""",
"""000700800
006000031
040002000
024070000
010030080
000060290
000800070
860000500
002006000""",
"""001007090
590080001
030000080
000005800
050060020
004100000
080000030
100020079
020700400""",
"""000003017
015009008
060000000
100007000
009000200
000500004
000000020
500600340
340200000""",
"""300200000
000107000
706030500
070009080
900020004
010800050
009040301
000702000
000008006"""]


jugar(MAPAS[randint(0, len(MAPAS) - 1)])