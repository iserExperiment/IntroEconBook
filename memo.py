A = {1:100,2:100,3:300,4:200}
list(A.values())
A_1=list(A.items())
[i[0] for i in A_1 ]

{ A[i]:i for i in A }

dic2 = sorted(A.items(), key=lambda x:x[1])
{i[0]:i[1] for i in dic2}


list(A.values())
B = sorted(A, reverse=True)
[A[i] for i in B]

sorted(A.items(), key=lambda x:x[1])
sorted({p:p for p in A if p > 2}, reverse=True)      

if(len(tmp)!=0 and tmp[0]==","){

}

tmp=""

tmp=",9,2,3"
tmp=tmp.split(",")
[ i for i in tmp if i!="" ]
if len(tmp)!=0:
    print("a")
else: 
    print("b")

A

B
C = {p:{"a":p+1,"b":p+2} for p in B}
sorted(A.items(), key=lambda x:x[1], reverse=True)

D = sorted(C.items(), key=lambda x: x["a"], reverse=True)

sorted({1:"a",3:"b",2:"c"})
