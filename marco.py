#-------------------------------------------------------------------------------
# Name:        marco
# Purpose:
#
# Author:      MarcRobin
#
# Created:     23/10/2018
#-------------------------------------------------------------------------------

import tkinter
import time
import threading

def main():

    def get_text(event):
        if (entree.get().strip() != "") :
            print(event) #del
            print(entree.get()) #del
            canvas_chat.create_text(100,20,fill="blue",font="Times 12",text=entree.get()) #del
            messages.config(state=tkinter.NORMAL)
            messages.insert(tkinter.END, '%s\n' % entree.get(), "me")
            messages.config(state=tkinter.DISABLED)
            messages.see(tkinter.END)
            canvas_chat.update() #del
            print(entree.get().encode())
            global conn
            conn.send(entree.get().encode())
        entree.delete(0, 'end')


    conn()

    window = tkinter.Tk()
    label = tkinter.Label(window, text="Chat IoT")
    label.pack()

    canvas_chat = tkinter.Canvas(window, width=250, height=100, bg='ivory') #del
    canvas_chat.create_text(100,10,text="") #del
    #canvas_chat.pack(side=tkinter.TOP, padx=5, pady=5) #del
    messages = tkinter.Text(window, bg='ivory')
    messages.tag_config("me", foreground="blue", font="Times 12")
    messages.tag_config("othersname", foreground="black", font="Consolas 12")
    messages.tag_config("others", foreground="black", font="Times 12")
    messages.tag_config("privateme", foreground="blue", font="Times 12 italic")
    messages.tag_config("privateothers", foreground="black", font="Times 12 italic")
    messages.config(state=tkinter.DISABLED)
    messages.pack(side=tkinter.TOP, padx=10, pady=10)

    entree = tkinter.Entry(window, width=30)
    entree.pack(side=tkinter.BOTTOM, padx=5, pady=5)

    window.bind('<Return>', get_text)
    #window.after(1, getmsg)
    getmsgs = GetMsg(conn, window)
    getmsgs.daemon = False
    getmsgs.start()
    print(window.winfo_children()) #del
    for i in window.winfo_children() :#del
        print(i)#del
    window.mainloop()

    #time.sleep(2000)

    conn.send(b" ")
    time.sleep(1) #del
    getmsgs.stop()
    print("Fermeture de la connexion")
    conn.close()

def conn():
    import socket
    import sys

    hote = "localhost"
    port = 5000

    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((hote, port))
    except:
        print("ERREUR SYSTEME:", sys.exc_info()[0])
        print ("Echec de la connexion avec le serveur sur le port {}". format(port))
        sys.exit(1)

    print ("Connexion établie avec le serveur sur le port {}". format(port))
    print("#####",conn,"#####")
    print(conn.getsockname())

def getmsg(): #del
    msg_recu = conn.recv(1024)
    print(msg_recu.decode())
    messages.config(state=tkinter.NORMAL)
    messages.insert(tkinter.END, '%s\n' % entree.get(), "others")
    messages.config(state=tkinter.DISABLED)
    window.after(100000, getmsg)

class GetMsg(threading.Thread):

    def __init__(self, connexion, window):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.window = window
        self.stopevent = threading.Event()
    def run(self):
        while not self.stopevent.isSet() :
            msg_rec = self.connexion.recv(1024)
            print("other:", msg_rec.decode())
            for widg in self.window.winfo_children() :
                if isinstance(widg, tkinter.Text) :
                    widg.config(state=tkinter.NORMAL)
                    widg.insert(tkinter.END, '%s\n' % msg_rec.decode(), "others")
                    widg.config(state=tkinter.DISABLED)
    def stop(self):
        self.stopevent.set()


if __name__ == '__main__':
    main()


#http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
#https://python.developpez.com/cours/TutoSwinnen/?page=Chapitre8
#https://openclassrooms.com/forum/sujet/tkinter-entry-get?page=1
#https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
#https://stackoverflow.com/questions/17736967/python-how-to-add-text-inside-a-canvas
#https://stackoverflow.com/questions/42062391/how-to-create-a-chat-window-with-tkinter
#https://www.tutorialspoint.com/python/tk_text.htm
#https://stackoverflow.com/questions/47591967/changing-the-colour-of-text-automatically-inserted-into-tkinter-widget
#https://stackoverflow.com/questions/811532/how-to-scroll-automatically-within-a-tkinter-message-window
#https://stackoverflow.com/questions/13832720/how-to-attach-a-scrollbar-to-a-text-widget   !!!! pas appliqué
#https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only
#https://stackoverflow.com/questions/27645460/python-tkinter-text-insert-current-cursor
#http://effbot.org/tkinterbook/text.htm
#https://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
#https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/2235545-la-programmation-parallele-avec-threading


#prompt personne d'entrer son psuedo (noter les adresses ip, pour éviter les usurpations)
#faire un fichier de log de messages




