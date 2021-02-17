try:
    import cv2
    import numpy as np
except:
    print("Install opencv2 by typing : 'pip install opencv-python'")
    exit()

line_color = [0, 0, 255]
line_thickness = 1
dot_color = [255, 0, 0]
dot_size = 6






cap1 = cv2.VideoCapture("input.avi")



while True:
    try:
    
        ret, frame = cap1.read()
    
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect edges
        edges = cv2.Canny(gray, 40, 700)
        
        
        # get lines
        # (x1, y1, x2, y2)
        lines = cv2.HoughLinesP(
            edges,
            rho=1.5,
            theta=np.pi/180,
            threshold=50,
            minLineLength=80,
            maxLineGap=40        
        )
        
        selected = []
        selected2 = []
        
        for line in lines:
            #Horizontal lines detection
            for x1, y1, x2, y2 in line:
                if 260<y1<380:
                    pente = (y2 - y1)/(x2 - x1)
                    pente = abs(pente)
                    
                    if 0<=pente<=0.1:
                        selected.append([[x1, y1, x2, y2]])
            #Vertical lines detection
            for line in lines:
                for x1, y1, x2, y2 in line:
                    if 100<x1<500 and y1<200:
                        pente = (y2 - y1)/(x2 - x1)
                        pente = abs(pente)
                            
                        if pente>4:
                            selected2.append([[x1, y1, x2, y2]])
                        
                        
        selected = np.array(selected)
        selected2 = np.array(selected2)
        
        #Lay-off of the image
        cleaned_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
        
        #defining the lines properties
        line_color = [0, 0, 255]
        line_thickness = 1
        dot_color = [255, 255, 255]
        dot_size = 6
        
        #The pantograph lines filtering:
        Y1 = []
        for line in selected:
            for x1, y1, x2, y2 in line:
                Y1.append(y1)   
        
        y1max = min(Y1)
        pantograph = []
        for line in selected:
            for x1, y1, x2, y2 in line:
                if y1max == y1:
                    pantograph.append(line)
        
        pantograph = list(pantograph[0][0])
                
        
        
        #Drawing pantograph line
        '''cv2.line(cleaned_img, (pantograph[0], pantograph[1]), (pantograph[2], pantograph[3]), [0, 255, 0], 3)'''
        
        #Drawing Catenary lines
        '''for line in selected2:
            for x1, y1, x2, y2 in line:
                cv2.line(cleaned_img, (x1, y1), (x2, y2), line_color, line_thickness)'''
        
        
        ########### CONTACT POINT DETECTION #######################
        def point(line):
            p1 = (line[0][0], line[0][1])
            p2 = (line[0][2], line[0][3])
            return p1, p2
        
        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C
        
        def intersection(ligne1, ligne2):
            p1, p2 = point(ligne1)
            d1, d2 = point(ligne2)
            L1 = line(p1, p2)
            L2 = line(d1, d2)
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return int(x),int(y)
            else:
                return False
        
        #Pantogrph/catenary contact point
        contact = intersection(np.array(pantograph).reshape((1, 4)), selected2[0])

        cv2.circle(cleaned_img, contact, dot_size, dot_color, -1)
        
        
        
        #Overlaying lines on the original frame
        overlay = cv2.addWeighted(frame, 0.8, cleaned_img, 1.0, 0.0)
        cv2.imshow("Result", overlay)
    
    
        if cv2.waitKey(1) and 0xFF== ord('q'):
            break
    except:
        try:
            cv2.imshow("Result", frame)
            if cv2.waitKey(1) and 0xFF== ord('q'):
                break
        except:
            print('Fin de la video')
            break

cv2.destroyAllWindows()

