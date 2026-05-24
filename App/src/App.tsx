import { useState, useRef, useCallback } from "react"
import type { OcrResult, ApiResponse } from "./api/type"
import { createReceipt } from "./api/receiptApi";
import "./App.css"

function App() {
    // ── State ──────────────────────────────────────────────────────────────────

    // Set date
    const [date, setDate] = useState("");
    // Store the file selected or dropped by the user
    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    // Hold the OCR result returned from the API (null = no result yet)
    const [ocrResult, setOcrResult] = useState<OcrResult | null>(null)

    // Track loading state while the request is in-flight
    const [isLoading, setIsLoading] = useState(false)

    const [isSaving, setIsSaving] = useState(false);
    const [isDone, setIsDone] = useState(false);

    // Toggle the "dragover" CSS class on the drop zone
    const [isDragOver, setIsDragOver] = useState(false)

    // ── Ref ────────────────────────────────────────────────────────────────────
    // Reference to <input type="file"> — used to programmatically trigger the file dialog
    const fileInputRef = useRef<HTMLInputElement>(null)

    // ── Helpers ────────────────────────────────────────────────────────────────

    /** Convert bytes to a human-readable size string, e.g. "1.2 MB" */
    const formatSize = (bytes: number): string => {
        if (bytes < 1024)        return bytes + ' B'
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    }

    /** Update state when the user selects a file (both via dialog and drag-drop) */
    const handleFileSelect = useCallback((file: File | null) => {
        if (!file) return
        setSelectedFile(file)  // Store the file in state instead of direct DOM manipulation
        setOcrResult(null)     // Clear the previous result whenever a new file is chosen
    }, [])

    // ── Event Handlers ─────────────────────────────────────────────────────────

    /** Fired when the user picks a file through the native file dialog */
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        handleFileSelect(e.target.files?.[0] ?? null)
    }

    /** Prevent default browser behaviour so the drop event works, and add the highlight class */
    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault()
        setIsDragOver(true)
    }

    /** Remove the highlight class when the dragged item leaves the drop zone */
    const handleDragLeave = () => {
        setIsDragOver(false)
    }

    /** Accept the file that was dropped onto the drop zone */
    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault()
        setIsDragOver(false)

        const file = e.dataTransfer.files[0]  // Only take the first dropped file
        handleFileSelect(file ?? null)
    }

    // ── OCR Request ────────────────────────────────────────────────────────────

    /** Send the selected file to the /ocr endpoint and display the result */
    const runOCR = async () => {
        if (!selectedFile) {
            alert('Please select a file first.')
        return
        }

        setIsLoading(true)
        setOcrResult(null)

        // Build FormData to send the file as multipart/form-data
        const formData = new FormData()
        formData.append('file', selectedFile)

        try {
        const response = await fetch('/ocr', {
            method: 'POST',
            body: formData,
        })

        const data: ApiResponse = await response.json()
        console.log(data.result)

        // Save the result to state — React will re-render automatically
        setOcrResult(data.result)

        } catch (error) {
            console.error(error)
            alert('Upload failed')
        } finally {
            // Always turn off the loading indicator, whether the request succeeded or failed
            setIsLoading(false)
        }
    }

    const handleAddd = async () => {

        if (!date) {
            alert("Please select date");
            return;
        }

        if (!ocrResult) {
            alert("Value receipt not found.")
            return;
        }

        try {
            await createReceipt({
                date: date,
                bank: ocrResult.bank,
                detail: "",
                income: 0,
                expenses: ocrResult.amount,
            });

            //console.log("Success");
            setIsDone(true);

        } catch (error) {
            console.error(error);
        
        }finally {

            setIsSaving(false);
        
        }
    };

    // ── OCR Result Text ────────────────────────────────────────────────────────

    /**
     * Compute the text to display inside #ocrResult:
     *   - Default (no action) → "Detail receipt."  (matches the original HTML prototype)
     *   - While loading       → "Processing OCR…"
     *   - Result available    → "Bank: ... | Amount: ..."
     */
    const getOcrDisplayText = (): React.ReactNode => {
        if (isLoading) return 'Processing OCR…'
        if (ocrResult) return (
            <>
            <strong>Bank:</strong> {ocrResult.bank}
            <br />
            <strong>Amount:</strong> {ocrResult.amount}
            </>
        )
        return 'Detail receipt.'  // Placeholder matching the original HTML prototype
    }

    // ── Render ─────────────────────────────────────────────────────────────────
    return (
        <div className="card">

            {/* ── Header ── Text matches the original HTML prototype exactly */}
            <header>
                <div className="label-tag">DEMO Read Receipt</div>
                <h1>Upload receipt</h1>
            </header>

            <div className="add-date">
                <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                />

            </div>

            {/* ── Drop Zone ──
                The <input> is stacked over the entire zone via CSS
                (position: absolute; inset: 0; opacity: 0), so clicking
                anywhere inside the zone opens the file dialog.
            */}
            <div
            className={`drop-zone${isDragOver ? ' dragover' : ''}`}
            id="dropZone"
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="fileInput"
                    name="file"
                    accept="image/*,.pdf"
                    ref={fileInputRef}
                    onChange={handleInputChange}
                />

                {/* Copy text matches the original HTML prototype */}
                <p className="drop-title">Drop your file here</p>
                <p className="drop-sub">or <span>browse to upload</span></p>
            </div>

            {/* ── File Info ──
                Shows the file name once selected, or "No file selected" otherwise.
                The "has-file" class changes the colour via CSS.
            */}
            <p
            className={`file-info${selectedFile ? ' has-file' : ''}`}
            id="fileInfo"
            >
            {selectedFile
                ? `${selectedFile.name}  (${formatSize(selectedFile.size)})`
                : 'No file selected'}
            </p>

            {/* ── OCR Result ──
                Renders the placeholder / loading text / result inside the same element
                (no conditional mounting) to stay consistent with the original HTML
                prototype that always has #ocrResult in the DOM.
            */}
            <div className="info-read">
                <div className="inforeceipt">
                    <p
                        className={`file-info${ocrResult ? ' has-file' : ''}`}
                        id="ocrResult"
                    >
                        {getOcrDisplayText()}
                    </p>
                </div>
                
                <div className={`add-info${ocrResult ? ' read-done' : ''}`}>
                    <button 
                        className="btn" 
                        onClick={handleAddd}
                        disabled={isSaving}
                        
                    >
                        {isSaving
                            ? 'Adding...'
                            : isDone
                                ? 'Add done'
                                : '+ Add data'
                        }
                                                
                    </button>
                </div>

            </div>
            {/* ── Run OCR Button ── Label "Read File" matches the original HTML prototype */}
            <button
            className="btn btn-upload"
            id="uploadBtn"
            onClick={runOCR}
            disabled={isLoading}
            >
                {isLoading ? 'Processing…' : 'Read receipt'}
            </button>

            {/* ── Footer ── Text matches the original HTML prototype */}
            <p className="footer-note">
                Supported: PNG, JPG, PDF &nbsp;·&nbsp; Max 10 MB
            </p>

        </div>
    )
}

export default App