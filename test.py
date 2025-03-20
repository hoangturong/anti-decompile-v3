from anti import protect_main


antii = protect_main()

@antii
def main():
    print('Hello World')
    input('Press Enter to exit: ')

if __name__ == "__main__":
    main()
