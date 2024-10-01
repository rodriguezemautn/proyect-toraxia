import React, { useState } from 'react';
import { Upload, message, Button, Spin, Alert } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Dragger } = Upload;

const ImageUpload = () => {
  const [loading, setLoading] = useState(false);
  const [validationResult, setValidationResult] = useState(null);

  const handleUpload = async (info) => {
    const { file } = info;
    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    try {
      const response = await axios.post('/api/validation/validate/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setValidationResult(response.data);
      if (response.data.is_valid) {
        message.success('Imagen validada correctamente');
      } else {
        message.warning('La imagen no es válida');
      }
    } catch (error) {
      message.error('Error al validar la imagen');
    } finally {
      setLoading(false);
    }
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76', // Reemplazar con tu endpoint real
    onChange: handleUpload,
    accept: 'image/*'
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <Dragger {...uploadProps}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Haz clic o arrastra una imagen para subirla</p>
        <p className="ant-upload-hint">
          Solo se permiten imágenes de radiografías frontales de tórax
        </p>
      </Dragger>
      
      {loading && <Spin tip="Validando imagen..." style={{ marginTop: '20px' }} />}
      
      {validationResult && (
        <Alert
          message={validationResult.is_valid ? "Imagen Válida" : "Imagen No Válida"}
          description={validationResult.message}
          type={validationResult.is_valid ? "success" : "warning"}
          showIcon
          style={{ marginTop: '20px' }}
        />
      )}
      
      {validationResult && validationResult.is_valid && (
        <Button
          type="primary"
          style={{
            marginTop: '20px',
            backgroundColor: '#00b1c7',
            borderColor: '#00c2db'
          }}
        >
          Continuar con la Clasificación
        </Button>
      )}
    </div>
  );
};

export default ImageUpload;
