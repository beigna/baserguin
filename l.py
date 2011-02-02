from collector.worker import PartedQueue

pq = PartedQueue()

for a in [1,2,3,4,5,6,7,8,9,0]:
    pq.put('a', a)

for a in ['a','b','c','d','e','f','g','h','i','j']:
    pq.put('b', a)

for a in ['hola', 'chau', 'buen dia', 'buenas noches', 'good morning, ehh']:
    pq.put('c', a)

for a in range(6):
    print pq.get()
