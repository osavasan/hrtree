from hr.tree import Tree 
import logging

def main():
    logging.getLogger().setLevel(logging.INFO)
    input_file = input("Input File (input.json):")
    hr_tree = Tree()
    hr_tree.load_file(input_file if input_file else "input.json")
    hr_tree.show()
    print(f"Total salary: {hr_tree.total_salary()}")
    
if __name__ == '__main__':
    main()