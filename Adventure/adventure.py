from flask import Flask, url_for, request, redirect, render_template, session
import sys


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'QQiV3dyYLpPOpdcjfh-5-Q'
outputs = ""
numInput = ""
Char = ""
num = ""
x = []
Item = ""
cas = 0
invCount = ""
listAdd = ""
modItem = ""
textDisp = ""
AdamInventory = ['Spoon', 'Fork', 'Knife']
SaraInventory = ['Book', 'Laptop', 'Water']
MorganInventory = ['Necklace', 'Pizza', 'Phone']
CharacterIndex = ['Adam', 'Sara', 'Morgan']
ItemIndex = [AdamInventory, SaraInventory, MorganInventory]

@app.route("/", methods=['GET', 'POST'])
def Intro():
    global outputs
    global numInput
    global textDisp
    numInput = ""
    if request.method == 'POST':
        numInput = request.form['numInput']
        try:
            if int(numInput) == 1:
                return redirect(url_for('Results'))
            elif int(numInput) == 2:
                return redirect(url_for('Results'))
            elif int(numInput) == 3:
                return redirect(url_for('addCharacter'))
            elif int(numInput) == 4:
                return redirect(url_for('Results'))
            elif int(numInput) == 5:
                return redirect(url_for('Results'))
            else:
                textDisp = "Please choose an integer between 1 and 5"
                return redirect(url_for('nope'))
        except ValueError:
            textDisp = "Please choose an integer between 1 and 5"
            return redirect(url_for('nope'))
            
    else:
        outputs = '''
            <p>These are your options:</p>
            <p>1: Print a character's inventory</p>
            <p>2: Add to a character's inventory</p>
            <p>3: Add a new character</p>
            <p>4: Remove from inventory</p>
            <p>5: Modify a character's inventory</p>
            <p>Type Ctrl-C in Command Prompt to quit!</p>
            <p>What would you like to do? Enter an integer between 1 and 5:</p>
            '''
       
        return render_template('renderInventor.html', outputs = outputs)
        
@app.route('/no', methods=['GET', 'POST'])
def nope():
    global textDisp
    if request.method == 'POST':
        return redirect(url_for('Intro'))
    else:
        return render_template('followInstructions.html', textDisp=textDisp)
        
    
@app.route('/test', methods=['GET', 'POST'])
def Results():
    global CharacterIndex
    global Char
    global numInput
    global textDisp
    if request.method == 'POST':
        Char = request.form['Char'].capitalize()
        if Char in CharacterIndex:
            if int(numInput) == int(2):
                return redirect(url_for('addInventory'))
            elif int(numInput) == int(1):
                return redirect(url_for('showInventory'))
            elif int(numInput) == int(4):
                return redirect(url_for('invRemove'))
            elif int(numInput) == int(5):
                return redirect(url_for('modifyInv'))
            else:
                return redirect(url_for('Intro'))
        else:
            textDisp = "This is not a character."
            return redirect(url_for('nope'))
    else:
        return render_template('DispCharacter.html', CharacterIndex=CharacterIndex)
        
@app.route('/ROUS', methods=['GET', 'POST'])
def showInventory():
    global Char
    global x
    x.clear()
    num = len(ItemIndex[CharacterIndex.index(Char)])
    x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
    if request.method == "POST":
        return redirect(url_for('Intro'))
    else:
        while num > 1:
            num = num - 1
            x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
            print(x)
        return render_template('ShowInventory.html', Char=Char, num=num, ItemIndex=ItemIndex, CharacterIndex=CharacterIndex, x=x)
    
@app.route('/42', methods=['GET', 'POST'])
def addInventory():
    global Char
    global Item
    if request.method == "POST":
        Item = request.form['Item'].capitalize()
        ItemIndex[CharacterIndex.index(Char)].append(Item)
        return redirect(url_for('showInventory'))
    else:
        return render_template('AddInventory.html', Char=Char)
    


@app.route('/alzabo', methods=['GET', 'POST'])
def addCharacter():
    global Char
    if request.method == "POST":
        Char = request.form['nuChar'].capitalize()
        if Char in CharacterIndex:
            textDisp = str(Char + " is already a character.")
            return redirect(url_for('nope'))
        else:
            CharacterIndex.append(Char)
            ItemIndex.append([])
            return redirect(url_for('howManyItems'))
    else:
        return render_template('addChar.html')
      
@app.route('/LetoII', methods=['GET', 'POST'])
def howManyItems():
    global Char
    global ItemIndex
    global invCount
    global textDisp
    global CharacterIndex
    if request.method == "POST":
        try:
            invCount = int(request.form['ItemNum'])
            if invCount > 0:
                return redirect(url_for('defItems'))
            else:
                textDisp = "Impossible number of items."
                CharacterIndex.remove(Char)
                return redirect(url_for('nope'))
        except ValueError:
            textDisp = "Not an integer!"
            CharacterIndex.remove(Char)
            return redirect(url_for('nope'))
    else:
        return render_template('howmanyitems.html')
          
@app.route('/dunno', methods=['GET', 'POST'])
def defItems():
    global listAdd
    global ItemIndex
    global cas
    global invCount
    if request.method == "POST":
        listAdd = request.form['listAdd'].capitalize()
        ItemIndex[-1].append(listAdd)
        invCount = invCount - 1
        return redirect(url_for('buffer'))
    else:
        return render_template('defineitems.html')

@app.route('/buffer')
def buffer():
    if invCount > 0:
        return redirect(url_for('defItems'))
    else:
        return redirect(url_for('showInventory'))
        
@app.route('/remove', methods=['GET', 'POST'])
def invRemove():
    global Char
    global x
    global textDisp
    x.clear()
    num = len(ItemIndex[CharacterIndex.index(Char)])
    x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
    if request.method == "POST":
        remItem = request.form['remItem'].capitalize()
        if remItem in ItemIndex[CharacterIndex.index(Char)]:
            if len(ItemIndex[CharacterIndex.index(Char)]) == 1:
                textDisp = "Characters must have at least one item in their inventory"
                return redirect(url_for('nope'))
            else:
                ItemIndex[CharacterIndex.index(Char)].remove(remItem)
                return redirect(url_for('showInventory'))
        else:
            textDisp = "Invalid item."
            return redirect(url_for('nope'))
    else:
        while num > 1:
            num = num - 1
            x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
        return render_template('removeinventory.html', Char=Char, x=x)
        
@app.route('/mod', methods=['GET', 'POST'])
def modifyInv():
    global Char
    global x
    global modItem
    global ItemIndex
    global CharacterIndex
    x.clear()
    num = len(ItemIndex[CharacterIndex.index(Char)])
    x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
    if request.method == "POST":
        modItem = request.form['modItem'].capitalize()
        return redirect(url_for('modifyInv2'))
    else:
        while num > 1:
            num = num - 1
            x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
        return render_template('inventorymod.html', Char=Char, x=x, ItemIndex=ItemIndex, CharacterIndex=CharacterIndex)
    
@app.route('/mod2', methods=['GET', 'POST'])
def modifyInv2():
    global Char
    global x
    global modItem
    global ItemIndex
    global CharacterIndex
    global textDisp
    x.clear()
    num = len(ItemIndex[CharacterIndex.index(Char)])
    x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
    if request.method == "POST":
        modItem2 = request.form['modItem2'].capitalize()
        if modItem in ItemIndex[CharacterIndex.index(Char)] and modItem2 in ItemIndex[CharacterIndex.index(Char)]:
            ItemIndex[CharacterIndex.index(Char)][ItemIndex[CharacterIndex.index(Char)].index(modItem)] = ItemIndex[CharacterIndex.index(Char)][0] 
            ItemIndex[CharacterIndex.index(Char)][0] = modItem
            ItemIndex[CharacterIndex.index(Char)][ItemIndex[CharacterIndex.index(Char)].index(modItem2)] = ItemIndex[CharacterIndex.index(Char)][1]
            ItemIndex[CharacterIndex.index(Char)][1] = modItem2
            return redirect(url_for('Intro'))
        else:
            textDisp = "Your inputs are not valid"
            return redirect(url_for('nope'))

    else:
        while num > 1:
            num = num - 1
            x.append(str(ItemIndex[CharacterIndex.index(Char)][num - 1]))
        return render_template('inventorymod2.html', Char=Char, x=x, ItemIndex=ItemIndex, CharacterIndex=CharacterIndex)