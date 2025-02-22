# celciuminput = int(input('Введите температуру в цельсиях: '))
# celciumoutput = celciuminput * 1.8 + 32
# print('температура в фаренгейтах:', celciumoutput)

from random import randint
answer = randint(0, 10)

print('я загадал число от 0 до 10, угадай. :)')
inpt = int(input('Введите ваше число'))

while inpt != answer:
    print('н угадал, пороуй снова')

    inpt = int(input('Введите ваше число'))

print('угадал')