import face_recognition
import cv2


def main():
    # This is a demo of running face recognition on a video file and saving the results to a new video file.
    #
    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Open the input movie file
    input_movie = cv2.VideoCapture(0)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    output_movie = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 360))

    # Load some sample pictures and learn how to recognize them.
    lmm_image = face_recognition.load_image_file("C:\\Users\\Thinkpad\\source\\repos\\py\\jikao\\21110112101443.JPG")
    lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

    known_faces = [
        lmm_face_encoding,
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0
    import datetime

    starttime = datetime.datetime.now()
    print(starttime)

    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

            # If you had more than 2 faces, you could make this logic a lot prettier
            # but I kept it simple for the demo
            name = None
            if match[0]:
                name = "Lin-Manuel Miranda"

            face_names.append(name)

        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue
            testImg = frame[top:bottom, left:right]
            #print("test.png")
            # Draw a label with a name below the face
            #cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


            for face_landmarks in face_recognition.face_landmarks(frame):
                for facial_feature in face_landmarks.keys():
                    for pt_pos in face_landmarks[facial_feature]:
                        cv2.circle(frame, pt_pos, 1, (255, 0, 0), 2)

        cv2.imshow("c", frame)
        # Write the resulting image to the output video file
        # print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    # All done!
    endtime = datetime.datetime.now()
    print(endtime)
    print((endtime - starttime).seconds)
    input_movie.release()
    output_movie.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    """
    a=face_recognition.load_image_file("C:\\Users\\Thinkpad\\source\\repos\\py\\jikao\\21110112101513.JPG")
    for face_landmarks in face_recognition.face_landmarks(a):
        for facial_feature in face_landmarks.keys():
            for pt_pos in face_landmarks[facial_feature]:
                cv2.circle(a, pt_pos, 1, (255, 0, 0), 2)
    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    cv2.imshow("asas",a)
    cv2.waitKey(0)"""
    main()