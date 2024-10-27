import time
import multiprocessing

def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    # ici on crée une piscine (Pool), qui assignera une tâche à un nombre donné de coeur
    # on peut préciser le nombre de coeur à employer. Par défaut, Pool() utilisera le nombre
    # maximal possible
    with multiprocessing.Pool() as pool:
        # map assigne la fonction a chaque valeur de l'iterable
        # chaque coeur réalise ensuite la tâche, puis en commence une autre
        pool.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5000000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")