from antii import protect_main


anti = protect_main()

@anti
def main():
    print('Hello World')
    input('Press Enter to exit: ')

if __name__ == "__main__":
    main()