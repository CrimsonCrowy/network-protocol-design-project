from tkinter import *

class chatModule():
    def __init__(self):
        #RootWindow
        self.window = Tk()
        self.window.title("Will work for packets!")
        #Messages Container
        self.messages = Text(self.window)
        self.messages.pack()
        #Input for user messgaes
        self.userInput = StringVar()
        self.inputeField = Entry(self.window, text=self.userInput)
        self.inputeField.pack(side=BOTTOM, fill=X)
        #Button for file sendind
        self.sendFileButton = Button(self.window, text="File", command=self.sendFile)
        self.sendFileButton.pack(side=RIGHT)
        #Field for input for file send
        self.filePath = StringVar()
        self.filePath.set("Input your file path here")
        self.filePathField = Entry(self.window, text=self.filePath)
        self.filePathField.pack(side=BOTTOM, fill=X)
        #Recipient field adjuster
        self.recipient = StringVar()
        self.recipient.set("Recipient?")
        self.recipientField = Entry(self.window, text=self.recipient)
        self.recipientField.pack(side=BOTTOM, fill=X)


    #Gets absolute path and makes payload. Need to figure out how to allign a darn new input field for the File path
    def sendFile(self):
        getFilePath = self.filePathField.get()
        getRecipient = self.recipientField.get()

        # For debugging use, Delete later?
        print("I got this absolute path " + getFilePath)
        payload = ""

        try:
            f = open(getFilePath, "r")
        except:
            #Literally needs extension as well when trying to open, be careful. Not hardcoding ".txt" for versitility
            self.messages.insert(INSERT, "AdminControls: Looks like the file you just attempted to open does not exist!\n")
            print("Looks like that file did not want to open.")
        absolutepath = getFilePath.split("\\")
        payload = payload + "FILE|" + absolutepath[len(absolutepath) - 1] + "&"
        for l in f:
            payload = payload + l

        #Add the function that takes care of packet sending. payload is a string, not sure where we add recipient field for packet
        # For debugging use, Delete later?
        print(payload)
        self.filePath.set("Input your file path here")


    #Function for getting user input for the chat. Immidetly posts his and sends to packetsencd function
    def onEnterPress(self, event):
        getInput = self.inputeField.get()
        getRecipient = self.recipientField.get()

        print(getInput)
        self.messages.insert(INSERT, "You: ")
        self.messages.insert(INSERT, '%s\n' % getInput)
        self.userInput.set('')

        #Does the chat make this payload too? Or is just the string needed here?
        payload = ""
        payload = payload + getInput

        #For debugging use, Delete later?
        print(payload)

        return "break"

    #Simply appendsmessage from recieved packet? I have changed this to recieve a whole packet as an argument as I need to grab the sender as well
    def postRecievedMessage(self, packet):
        self.messages.insert(INSERT, packet.parts['srcNode'] + ": ")
        self.messages.insert(INSERT, packet.parts['payload'] + "\n") #Which part of the packet is a message
        #I think I need to specify if it was direct message or brodcasted toe everyone, but still didnt tell me what part of the packet does

    def startChat(self):
        self.frame = Frame(self.window)  # , width=300, height=300)
        self.inputeField.bind("<Return>", self.onEnterPress)
        self.frame.pack()

        self.window.mainloop()

chatBot = chatModule()
chatBot.startChat()