# A function that returns the length of the value:
def lenOfCar(e):
  return len(e)

cars = ['Suzuki', 'Audi', 'duccati', 'Polo']

cars.sort(key=lenOfCar)