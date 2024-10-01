import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import LoginForm from './components/LoginForm';
import AdministrativeView from './components/AdministrativeView';
import DoctorView from './components/DoctorView';
import TechnicianView from './components/TechnicianView';
import UserManagement from './components/UserManagement';
import AppointmentBooking from './components/AppointmentBooking';
import ReportGeneration from './components/ReportGeneration';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/" element={<Dashboard />}>
          <Route path="administrative" element={<AdministrativeView />} />
          <Route path="doctor" element={<DoctorView />} />
          <Route path="technician" element={<TechnicianView />} />
          <Route path="users" element={<UserManagement />} />
          <Route path="appointments" element={<AppointmentBooking />} />
          <Route path="reports" element={<ReportGeneration />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
