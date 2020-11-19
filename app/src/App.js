import React, {useState, useEffect} from 'react';
import axios from 'axios'
import './App.css';

function App() {
  const [gitUrl, setGitUrl] = useState('');
  const [output, setOutput] = useState([]);
  const [modelId, setModelId] = useState('');
  const handleGitUrl = (event) => {
    setGitUrl(event.target.value);
  }

  const onSubmit = async () => {
    let resp = await axios({
      "url": window.location.origin + "/api/create-model",
      "method": "POST",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "postman-token": "aa995fa2-3bb2-388b-57a2-f5772584c2ac"
      },
      "data": "{\n    \"url\": \"" + gitUrl + "\"\n}"
    });
    setModelId(resp.data);
  }

  useEffect(() => {

  }, [output])

  return (
    <div className="App">
      <div className="Input">
        <input id="text" placeholder="git@github.com:Adi2612/reading-comprehender.git" value={gitUrl} onChange={handleGitUrl} /> 
        <button type="submit" id="button" onClick={onSubmit} > Submit </button>
      </div>
      {modelId !== '' &&
      <div className="ModelId">
        {window.location.origin + "/api/inference/" + modelId}
      </div>}
      <div className="Show">
        {output.map((item, i) => (
          <div key={i} className="Item">
            {item}
          </div>
        ))}
        {output.length === 0 &&
        <div style={{textAlign: 'center', color: 'white'}}> Logs will appear here </div>
        }
      </div>
      <footer className="Footer">
        <div className="Start"> Made With</div>
        <div className="Love"> ❤️ </div>
      </footer>
    </div>
  );
}

export default App;
