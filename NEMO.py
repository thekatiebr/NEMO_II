import KnowledgeBase
import ML-Controller

		
def main():
	kb = KnowledgeBase("config/login_file.txt")
	kb.importData("data/SPECT.data", "data/SPECT.schema")
	#importData("config/login_file.txt", "data/SPECTF.data", "data/SPECTF.schema")

if __name__ == "__main__":
	main()
