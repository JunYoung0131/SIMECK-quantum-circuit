import numpy as np
from qiskit import *
from qiskit.providers.aer import QasmSimulator
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
from qiskit.transpiler.passes import BasisTranslator
from qiskit.converters import circuit_to_dag, dag_to_circuit

# 큐비트
qreg_q = QuantumRegister(96, 'q')

# 클래식 비트
creg_c = ClassicalRegister(32, 'c')

circuit = QuantumCircuit(qreg_q, creg_c)

#PlainText setting    
circuit.x(qreg_q[0])
circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[4])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[11])
circuit.x(qreg_q[13])
circuit.x(qreg_q[14])
circuit.x(qreg_q[16])
circuit.x(qreg_q[18])
circuit.x(qreg_q[21])
circuit.x(qreg_q[22])
circuit.x(qreg_q[24])
circuit.x(qreg_q[26])
circuit.x(qreg_q[29])
circuit.x(qreg_q[30])

#Key setting    
circuit.x(qreg_q[40])
circuit.x(qreg_q[51])
circuit.x(qreg_q[56])
circuit.x(qreg_q[59])
circuit.x(qreg_q[68])
circuit.x(qreg_q[72])
circuit.x(qreg_q[76])
circuit.x(qreg_q[83])
circuit.x(qreg_q[84])
circuit.x(qreg_q[88])
circuit.x(qreg_q[91])
circuit.x(qreg_q[92])

for r in range(0, 32):
    #XOR with R and (L and L<<5)
    for i in range(0, 16):
        if(i<5):
            circuit.ccx(qreg_q[i+16], qreg_q[i+16+11], qreg_q[i])
        else:
            circuit.ccx(qreg_q[i+16], qreg_q[i+16-5], qreg_q[i])

    circuit.barrier()        

    #XOR with R and (L<<1)
    for i in range(0, 16):
        if(i==0):
            circuit.cx(qreg_q[i+16+15], qreg_q[i])
        else:
            circuit.cx(qreg_q[i+16-1], qreg_q[i])

    circuit.barrier()  

    #XOR with R and K
    for i in range(0, 16):
        circuit.cx(qreg_q[i+32], qreg_q[i])

    circuit.barrier()  

    #Key schedule
    #XOR with K0 and (T0 and T0<<5)
    for i in range(32, 48):
        if(i<37):
            circuit.ccx(qreg_q[i+16], qreg_q[i+16+11], qreg_q[i])
        else:
            circuit.ccx(qreg_q[i+16], qreg_q[i+16-5], qreg_q[i])

    circuit.barrier()        

    #XOR with K0 and (L<<1)
    for i in range(32, 48):
        if(i==32):
            circuit.cx(qreg_q[i+16+15], qreg_q[i])
        else:
            circuit.cx(qreg_q[i+16-1], qreg_q[i])

    circuit.barrier()

    #XOR with K and C
    for i in range(34, 48):
        circuit.x(qreg_q[i])

    circuit.barrier()
    
    #XOR with Z
    if(r==0 or r==1 or r==2 or r==3 or r==4 or r==8 or r==9 or r==11 or r==12 or r==13 or r==15 or r==17 or r==22 or r==25 or r==27 or r==28 or r==31):
        circuit.x(qreg_q[32])
    
    circuit.barrier()
    
    #shift k, t_r, t_r+1, t_r+2
    for i in range(32, 48):
        circuit.swap(qreg_q[i+16], qreg_q[i])
        
    for i in range(48, 64):
        circuit.swap(qreg_q[i+16], qreg_q[i])
    
    for i in range(64, 80):
        circuit.swap(qreg_q[i+16], qreg_q[i])
    
    # switch r and l
    for i in range(0, 16):
        circuit.swap(qreg_q[i+16], qreg_q[i])
        
circuit.measure(range(32), range(32))

IBMQ.load_account()

qcomp=IBMQ.get_provider('ibm-q')
my_backend  = qcomp.get_backend('simulator_mps')

# job=execute(circuit, backend=my_backend)
result=execute(circuit, backend=my_backend).result()

counts = result.get_counts()
print(counts)