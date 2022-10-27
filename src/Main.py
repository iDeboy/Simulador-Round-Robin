from round_robin import PFrame, PPanel

def main():
    f = PFrame()
    f.Width = 1000
    f.Height = 700

    panel = PPanel()
    
    panel.Height = 100
    panel.Width = 50
    panel.x = 50
    panel.y = 50

    f.add(panel)

    f.show()
    

if __name__ == '__main__':
    main()