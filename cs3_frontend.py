from tkinter import *
import pymysql

conection = pymysql.Connect(
  host="localhost",
  port=3306,
  user="root",
  password="12345678",
  db="cs3"
)
cursor=conection.cursor()

    
raiz=Tk()
raiz.title("FORMULARIO")
raiz.resizable(0,0)
raiz.iconbitmap("l1.ico")
raiz.geometry("300x300")
raiz.config(bg="black")

correo=StringVar()
tema=StringVar()
detalle=StringVar()

cuadro1=Entry(raiz,textvariable=correo)
cuadro1.place(x=100,y=40)

label1=Label(raiz, text="Email: ")
label1.place(x=40,y=40)

cuadro2=Entry(raiz,textvariable=tema)
cuadro2.place(x=100,y=70)

label2=Label(raiz, text="Tema: ")
label2.place(x=40,y=70)

cuadro3=Entry(raiz,textvariable=detalle)
cuadro3.place(x=100,y=100,width=150,height=150)

label3=Label(raiz, text="Detalle: ")
label3.place(x=40,y=100)
def codbot():
    
    if correo.get()=="" or tema.get()=="" and detalle.get()=="":
        completado=Tk()
        completado.title("Error")
        completado.resizable(0,0)
        completado.iconbitmap("l1.ico")
        completado.geometry("300x100")
        fin=Label(completado, text=" los campos estan vacios",font=("Cambria",13))
        fin.place(x=50,y=30)
        completado.mainloop()
    else:
        a1=correo.get()
        a2=tema.get()
        a3=detalle.get()
        
        sql = "INSERT INTO formulario(email, tema, detalle) VALUES('"+a1+"','"+a2+"','"+a3+"')"
        cursor.execute(sql)
        conection.commit()
        
        
        completado=Tk()
        completado.title("COMPLETADO")
        completado.resizable(0,0)
        completado.iconbitmap("l1.ico")
        completado.geometry("300x100")
        fin=Label(completado, text="se guardo correctamente \n la informacion ",font=("Cambria",13))
        fin.place(x=50,y=30)
        completado.mainloop()
    
def codbot2():
    correo.set("")
    tema.set("")
    detalle.set("")
    
envio=Button(raiz,text="Enviar",command=codbot)
envio.place(x=100,y=260)

limpiar=Button(raiz,text="limpiar",command=codbot2)
limpiar.place(x=200,y=260)

raiz.mainloop()
