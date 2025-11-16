import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [employeesFile, setEmployeesFile] = useState(null);
  const [previousFile, setPreviousFile] = useState(null);
  const [message, setMessage] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!employeesFile) {
      setMessage('Please select employees CSV.');
      return;
    }
    const form = new FormData();
    form.append('employees_csv', employeesFile);
    if (previousFile) {
      form.append('previous_csv', previousFile);
    }

    try {
      const resp = await axios.post('http://127.0.0.1:8000/assign', form, {

      // const resp = await axios.post('/assign', form, {
        responseType: 'blob',
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const blob = new Blob([resp.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'secret_santa_assignments.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setMessage('Assignment successful — CSV downloaded.');
    } catch (err) {
      if (err.response && err.response.data) {
        try {
          const text = await err.response.data.text();
          setMessage('Error: ' + text);
        } catch {
          setMessage('Error performing assignment.');
        }
      } else {
        setMessage('Network or server error.');
      }
    }
  };

  return (
    <div style={{maxWidth:800, margin:'40px auto', fontFamily:'sans-serif'}}>
      <h1>Acme Secret Santa</h1>
      <form onSubmit={onSubmit}>
        <div>
          <label>Current Employees CSV (required)</label><br/>
          <input type="file" accept=".csv" onChange={e => setEmployeesFile(e.target.files[0])} />
        </div>
        <div style={{marginTop:10}}>
          <label>Previous Assignments CSV (optional)</label><br/>
          <input type="file" accept=".csv" onChange={e => setPreviousFile(e.target.files[0])} />
        </div>
        <div style={{marginTop:20}}>
          <button type="submit">Run Assignment</button>
        </div>
      </form>
      <div style={{marginTop:20}}>{message}</div>
      <hr/>
      <p>
        Expected employee CSV headers: <code>Employee Name,Employee EmailID</code>.
        Previous CSV headers: <code>Employee Name,Employee EmailID,Secret Child Name,Secret_Child_EmailID</code>.
      </p>
    </div>
  );
}

export default App;
