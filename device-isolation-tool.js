import React, { useState } from 'react';
import axios from 'axios'; // يجب تثبيت هذا المكتبة: npm install axios

/**
 * مكون أداة العزل الشبكي (Device Isolation Tool)
 * يهدف إلى إرسال طلبات للعزل أو الإلغاء عبر API.
 */
const DeviceIsolationTool = () => {
  const [deviceId, setDeviceId] = useState('');
  const [status, setStatus] = useState('Idle'); // Idle, Isolating, Connected_Restored
  const [message, setMessage] = useState('');

  // URL نقطة نهاية (Endpoint) الخادم الذي يقوم بالعمل الفعلي للعزل
  const API_BASE_URL = 'http://localhost:3001/api/network';

  /**
   * الدالة المسؤولة عن بدء عملية العزل.
   */
  const handleIsolateDevice = async () => {const handleIsolateDevice = async () => {
  if (!deviceId) {
    setMessage('.الرجاء إدخال معرف الجهاز أولاً');
    return;
  }

  setStatus('Isolating');
  setMessage(`...جاري محاولة عزل الجهاز: ${deviceId}`);

  try {
    // طلب عزل الجهاز من الخادم الخلفي
    const response = await axios.post(`${API_BASE_URL}/isolate`, { deviceId });

    if (response.data.success) {
      setStatus('Isolated');
      setMessage(` تم عزل الجهاز ${deviceId} بنجاح`);
    } else {
      setStatus('Error');
      setMessage(` فشل العزل: ${response.data.error || 'خطأ غير معروف في الخادم'}`);
    }
  } catch (error) {
    console.error("Error during API call:", error);
    setStatus('Error');
    setMessage(` فشل الاتصال بالخادم أو حدوث خطأ: ${error.message}`);
  }
};

    if (!deviceId) {
      setMessage('الرجاء إدخال معرف الجهاز أولاً.');
      return;
    }

    setStatus('Isolating');
    setMessage(`جاري محاولة عزل الجهاز: ${deviceId}...`);

    try {
      // 1. طلب العزل من الخادم الخلفي
      const response = await axios.post(`${API_BASE_URL}/isolate`, { deviceId });

      if (response.data.success) {
        setStatus('Isolating'); // أو يمكن تعيينه إلى 'Isolated' إذا كان هناك حالة محددة
        setMessage(`✅ تم العزل بنجاح للجهاز ${deviceId}. الحالة: ${response.data.details}`);
      } else {
        setStatus('Error');
        setMessage(`❌ فشل العزل: ${response.data.error || 'حدث خطأ غير معروف في الخادم.'}`);
      }

    } catch (error) {
      // التعامل مع أخطاء الاتصال بالخادم نفسه
      console.error("Error during API call:", error);
      setStatus('Error');
      setMessage(`❌ فشل الاتصال بالخادم أو حدوث خطأ: ${error.message}`);
    }
  };

  /**
   * الدالة المسؤولة عن إعادة توصيل الجهاز للشبكة الرئيسية (إلغاء العزل).
   */
  const handleRestoreConnection = async () => {
      if (!deviceId) {
          setMessage('الرجاء إدخال معرف الجهاز أولاً.');
          return;
      }

      setStatus('Restoring');
      setMessage(`جاري محاولة إعادة توصيل الجهاز: ${deviceId}...`);

      try {
           // 2. طلب إلغاء العزل من الخادم الخلفي
          const response = await axios.post(`${API_BASE_URL}/restore`, { deviceId });

          if (response.data.success) {
            setStatus('Connected');
            setMessage(`✅ تم إعادة توصيل الجهاز ${deviceId} بنجاح.`);
          } else {
             setStatus('Error');
            setMessage(`❌ فشل الإعادة: ${response.data.error || 'حدث خطأ غير معروف في الخادم.'}`);
          }

      } catch (error) {
           console.error("Error during API call:", error);
           setStatus('Error');
           setMessage(`❌ فشل الاتصال بالخادم أو حدوث خطأ: ${error.message}`);
       }
  };


  // تصميم بسيط للواجهة لتحسين القراءة (يمكن استبداله بـ Tailwind/MUI)
  const containerStyle = { padding: '20px', fontFamily: 'Arial, sans-serif' };
  const inputStyle = { padding: '10px', marginRight: '15px', border: '1px solid #ccc', borderRadius: '4px' };
  const buttonStyle = (color) => ({
    padding: '10px 20px',
    marginRight: '10px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    backgroundColor: color,
    color: 'white'
  });

  return (
    <div style={containerStyle} className="isolation-tool-container">
      <h1>🛡️ أداة عزل الشبكات</h1>
      <p>أدخل معرف الجهاز لتطبيق إجراءات العزل أو الاستعادة.</p>

      <div>
        <input
          type="text"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
          placeholder="أدخل ID الجهاز (مثل: PC-001)"
          style={inputStyle}
          disabled={status === 'Isolating' || status === 'Restoring'}
        />

        {/* زر العزل */}
        <button
            onClick={handleIsolateDevice}
            style={{ ...buttonStyle('red'), opacity: (status === 'Isolating') ? 0.6 : 1 }}
            disabled={!deviceId || status === 'Isolating'}
        >
          {status === 'Isolating' ? 'جاري العزل...' : '🔴 عزل الجهاز'}
        </button>

        {/* زر الاستعادة */}
         <button
            onClick={handleRestoreConnection}
            style={{ ...buttonStyle('green'), opacity: (status === 'Restoring') ? 0.6 : 1 }}
            disabled={!deviceId || status === 'Restoring'}
        >
          {status === 'Restoring' ? 'جاري الاستعادة...' : '🟢 استعادة الاتصال'}
        </button>
      </div>

      <hr style={{ margin: '20px 0' }} />

      <h2>الحالة الحالية</h2>
      <p><strong>الوضع العام:</strong> <span style={{ fontWeight: 'bold', color: status === 'Error' ? 'red' : (status === 'Isolating' || status === 'Restoring') ? '#FF9800' : 'green' }}>{status}</span></p>
      <p><strong>الرسالة/التفاصيل:</strong> {message}</p>
    </div>
  );
};

export default DeviceIsolationTool;