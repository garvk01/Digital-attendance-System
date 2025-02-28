// Wait for DOM to load before running script
document.addEventListener("DOMContentLoaded", function () {
    const startBtn = document.getElementById("startRecognitionBtn");
    const markBtn = document.getElementById("markAttendanceBtn");
    const video = document.getElementById("camera");

    // Function to start face recognition (camera access)
    function startRecognition() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                console.log("Camera started for face recognition.");

                // Enable Mark Attendance button
                markBtn.classList.add("enabled");
                markBtn.disabled = false;
            })
            .catch(function (error) {
                console.error("Error accessing camera: ", error);
                alert("Could not access the camera. Please check permissions.");
            });
    }

    // Function to mark attendance
    function markAttendance() {
        if (!video.srcObject) {
            alert("Please start face recognition first!");
            return;
        }

        // Simulate attendance marking
        alert("Attendance marked successfully!");
        
        // Here, you can send data to a backend API (example)
        /*
        fetch('/mark-attendance', {
            method: 'POST',
            body: JSON.stringify({ userId: '12345', timestamp: new Date() }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => console.log("Attendance marked:", data))
        .catch(error => console.error("Error marking attendance:", error));
        */
    }

    // Add event listeners to buttons
    startBtn.addEventListener("click", startRecognition);
    markBtn.addEventListener("click", markAttendance);
});
