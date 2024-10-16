import React, {useState} from 'react';
import './ImageHandler.css';
import {SnackbarProvider, useSnackbar} from 'notistack';

const ImageHandler: React.FC = () => {
    const {enqueueSnackbar} = useSnackbar();

    const [imageSrc, setImageSrc] = useState('');
    const [identified, setIdentified] = useState<any>();

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadMessage, setUploadMessage] = useState<string>('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setSelectedFile(file);
            setUploadMessage('');

            setImageSrc('');
            setIdentified(null);
        } else {
            setSelectedFile(null);
            setUploadMessage('Please select a valid image file.');
        }
    };

    const convertToUrl = (localPath:any) => `http://localhost:5008${localPath.replace(/\\/g, '/').replace('./', '/')}`;

    const handleUpload = async () => {
        if (!selectedFile) {
            setUploadMessage('No file selected');
            return;
        }

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('http://localhost:5008/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                setUploadMessage(`Error uploading image: ${errorData.error}`);
            } else {
                const data = await response.json();

                fetch("http://127.0.0.1:5008/recognize", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({imgPath: data.image_path}),
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Success:', data);
                        setIdentified(data);
                        setImageSrc(convertToUrl(data.imgPath));
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        enqueueSnackbar('Error:'+ error, {variant: 'error'});
                    });
                setUploadMessage(`Image uploaded successfully`);
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            enqueueSnackbar('Error:'+ error, {variant: 'error'});
            setUploadMessage('Unexpected error occurred during upload.');
        }
    };

    return (
        <div className="upload-container">

            <h1 className="title">Celebrity Recognition</h1>
            <input type="file" className="file-input" accept="image/*" onChange={handleFileChange} />
            <button className="upload-button" onClick={handleUpload}>Upload</button>
            {uploadMessage && <p className="upload-message">{uploadMessage}</p>}

            {imageSrc && (
                <div className="img-container">
                    <img src={imageSrc} alt="Uploaded" style={{width: '300px', height: 'auto'}}/>
                </div>
            )}
            {identified &&
                <div>
                    <label><b>Person:</b>&nbsp;&nbsp;</label>
                    <label>{identified.person}</label>
                </div>
            }
        </div>
    );
};

export default ImageHandler;
