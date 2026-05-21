console.log("SCRIPT RUNNING");
const dropZone  = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo  = document.getElementById('fileInfo');

const ocrResult = document.getElementById("ocrResult");

// Show file name when user picks via browser dialog
fileInput.addEventListener('change', () => {
    showFileName(fileInput.files[0]);
    console.log(file);
    console.log(fileInput.files);
});

// Drag-over: add highlight class 
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();               // allow drop
    dropZone.classList.add('dragover');
});

// Drag-leave: remove highlight 
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

// Drop: read the dropped file
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    const file = e.dataTransfer.files[0];   // take first file only
    if (file) {
    // Sync the hidden input so FormData still works on submit
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;

    showFileName(file);
    }
});

// Display the selected file name 
function showFileName(file) {
    if (!file) return;
    fileInfo.textContent = `${file.name}  (${formatSize(file.size)})`;
    fileInfo.classList.add('has-file');
}

// Format bytes → human-readable size 
function formatSize(bytes) {
    if (bytes < 1024)        return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Upload handler (replace with real fetch/form logic)
async function runOCR() {

    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file first.');
        return;
    }
    console.log("running ocr...");

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("/ocr", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        //console.log(JSON.stringify(data, null, 2));
        //console.log(data);
        console.log(data.result);

        ocrResult.textContent = data.result; 

    } catch (error) {

        console.error(error);

        //alert("Upload failed");
    }
}