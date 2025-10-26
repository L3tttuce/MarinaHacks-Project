import json, datetime, os

class LogEmotion:
    def __init__(self, filename):
        self.filename = filename
    

    def loadJSON(self):
        try:
            with open(self.filename, "r", encoding = "utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def saveJSON(self, data):
        tmp = f"{self.filename}.tmp"
        with open(tmp, "w", encoding = "utf-8") as f:
            json.dump(data, f, indent = 4, ensure_ascii=False)
        os.replace(tmp, self.filename)

    def appendJSON(self, name, emotion, percentage):
        entry = {
            "name": name,
            "datetime": datetime.datetime.now().isoformat(),
            "emotion": emotion,
            "percentage": percentage
        }
        data = self.loadJSON()
        data.append(entry)
        self.saveJSON(data)
        return entry
            

def test():
    logger = LogEmotion("stats.json")

    logger.appendJSON("Bobby", "happy", 66)
    logger.appendJSON("Fat baby", "sad", 60)

#test()
