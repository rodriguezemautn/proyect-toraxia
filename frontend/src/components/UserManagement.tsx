import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message } from 'antd';
import { UserOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Option } = Select;

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingUser, setEditingUser] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users/');
      setUsers(response.data);
    } catch (error) {
      message.error('Error al cargar usuarios');
    }
  };

  const handleCreate = () => {
    setEditingUser(null);
    form.resetFields();
    setVisible(true);
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    form.setFieldsValue(user);
    setVisible(true);
  };

  const handleDelete = async (userId) => {
    try {
      await axios.delete(`/api/users/${userId}/`);
      message.success('Usuario eliminado');
      fetchUsers();
    } catch (error) {
      message.error('Error al eliminar usuario');
    }
  };

  const onFinish = async (values) => {
    try {
      if (editingUser) {
        await axios.put(`/api/users/${editingUser.id}/`, values);
        message.success('Usuario actualizado');
      } else {
        await axios.post('/api/users/', values);
        message.success('Usuario creado');
      }
      setVisible(false);
      fetchUsers();
    } catch (error) {
      message.error('Error al guardar usuario');
    }
  };

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Rol',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button icon={<EditOutlined />} onClick={() => handleEdit(record)} />
          <Button icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)} />
        </>
      ),
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <Button 
        type="primary" 
        onClick={handleCreate} 
        style={{ marginBottom: '20px', backgroundColor: '#00b1c7', borderColor: '#00c2db' }}
      >
        Crear Usuario
      </Button>
      <Table columns={columns} dataSource={users} />
      <Modal
        visible={visible}
        title={editingUser ? "Editar Usuario" : "Crear Usuario"}
        onCancel={() => setVisible(false)}
        footer={null}
      >
        <Form form={form} onFinish={onFinish} layout="vertical">
          <Form.Item name="username" label="Nombre de Usuario" rules={[{ required: true }]}>
            <Input prefix={<UserOutlined />} />
          </Form.Item>
          <Form.Item name="role" label="Rol" rules={[{ required: true }]}>
            <Select>
              <Option value="ADMIN">Administrador</Option>
              <Option value="MEDIC">Médico</Option>
              <Option value="TECH">Técnico RX</Option>
              <Option value="EMPLOYEE">Empleado Administrativo</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" style={{ backgroundColor: '#00b1c7', borderColor: '#00c2db' }}>
              Guardar
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserManagement;
