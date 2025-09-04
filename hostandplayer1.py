import socket

class player:
    def __init__(self):
        self.__name=""
        self.__data=""
    def set_name_and_data(self,name,data):
        self.__data=data
        self.__name=name
    def get_name(self):
        return self.__name
    def get_data(self):
        return self.__data


class tictactoe:
    def __init__(self,size):
        self.size=size 
        self.l=[]
        self.l1=[]
        for i in range(0,self.size):
            self.l1=list('-'*self.size)
            self.l.append(self.l1)
    
    def display(self):  
        k=0
        print("\n\t\t","----"*self.size)
        for i in range(0,self.size):
            print("\t\t|",end="")
            for j in range(0,self.size):
                print("",self.l[i][j],"|",end="")
                k+=1
            print("\n\t\t","----"*self.size)
        print("\n") 
        
    def assign(self,p,pos):
        while(1):
            if (self.l[(pos-1)//self.size][(pos-1)%self.size]=='-'):
                self.l[(pos-1)//self.size][(pos-1)%self.size]=p.get_data() 
                break
            else:
                print("Position is Already Occupied. Please Enter Another Position:")
                pos=int(input(f"{p.get_name()} Enter Your Position again :"))
                              
    def check(self):
        while True:
            X,O=0,0
            for i in self.l:   
                s=''
                for j in i:
                    s+=j
                if(s=='X'*self.size):
                    X=1
                    return 'X'
                elif(s=='O'*self.size):
                    O=1
                    return 'O'

            s1=''
            for j in range(0,self.size):   
                s1=''
                for i in self.l: 
                    s1+=i[j]
                if(s1=='X'*self.size):
                    X=1
                    return 'X'
                elif(s1=='O'*self.size):
                    O=1
                    return 'O'  

            s2=''
            for i in range(0,self.size):   
                 s2+=self.l[i][i]
            if(s2=='X'*self.size):
                X=1
                return 'X'
            elif(s2=='O'*self.size):
                O=1
                return 'O'
            
            s3=''
            r,c=0,(self.size-1)
            for i in range(0,self.size):   
                 s3+=self.l[r][c]
                 r=r+1
                 c=c-1
            if(s3=='X'*self.size):
                return 'X'
            elif(s3=='O'*self.size):
                return 'O'

            if(X==0):
                return "No"
            elif(O==0):
                return "No"
            
    def reset(self):
        self.l=[]
        self.l1=[] 
        for i in range(0,self.size):
            self.l1=list('-'*self.size)
            self.l.append(self.l1)


def board_to_string(board):
    return "\n".join(["".join(row) for row in board])

def string_to_board(board_str, size):
    rows = board_str.split("\n")
    return [list(row) for row in rows]


# create a socket (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8000))  
server_socket.listen(1)
print("Server listening on port 8000...")

# accepting connection
client_socket, addr = server_socket.accept()
print(f"Connected with {addr}")

while(1):
    a=input("To start game enter 1, To exit 0 : ")
    client_socket.send(a.encode())
    a=int(a)
    if(a!=1 and a!=0):
        print("Enter a valid Input")
    else:
        break

while(a==1):
    print("\n\n\t\t\tTICK TACK TOE\n")
    board_size=input("Enter the Board Size : ")
    client_socket.send(board_size.encode())
    board_size=int(board_size)
    cl=tictactoe(int(board_size))
    cl.reset()
    ps2=0
    p1=player()
    p2=player()
    a=input("Enter Player 1 Name : ")
    client_socket.send(a.encode())
    b=client_socket.recv(1024).decode()
    p1.set_name_and_data(a,"X")
    p2.set_name_and_data(b,"O")
    cl.display()

    for i in range((board_size*board_size//2)+1):
        # player 1 move
        p1_pos=input(f"{p1.get_name()} Enter Your Position (1-{board_size*board_size}) : ")
        client_socket.send(p1_pos.encode())
        cl.assign(p1,int(p1_pos))

        #updated board to Player 2
        client_socket.send(board_to_string(cl.l).encode())
        cl.display()

        if(cl.check()!="No"):
            print(f"\t\tWinner is {p1.get_name()} !\n\n ")
            break

        if(ps2 < (board_size*board_size)//2):
            # receive updated board from Player 2
            cl.l = string_to_board(client_socket.recv(4096).decode(), board_size)

            # Player 2 move
            p2_pos=int(client_socket.recv(4096).decode())
            cl.assign(p2,p2_pos)

            # Send updated board back to Player 2
            client_socket.send(board_to_string(cl.l).encode())
            cl.display()

            if(cl.check()!="No"):
                print(f"\t\tWinner is {p2.get_name()} !\n\n")
                break
            ps2+=1

    if cl.check()=="No":
        print("\t\tThe Match is a TIE ! \n\n")
    q=input("To start game enter 1, To exit 0 : ")
    client_socket.send(q.encode())
    a=int(q)
