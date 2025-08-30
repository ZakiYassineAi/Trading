import React from 'react';

const RiskWarning = () => (
  <div style={{
    backgroundColor: '#ffdddd',
    border: '1px solid #ff0000',
    color: '#d8000c',
    padding: '10px',
    margin: '10px 0',
    borderRadius: '5px',
    textAlign: 'center'
  }}>
    <strong>تحذير المخاطر:</strong> التداول ينطوي على مخاطر عالية وقد يؤدي إلى خسارة رأس المال. هذا المشروع هو أداة تعليمية وليس نصيحة استثمارية. لا تستثمر ما لا تستطيع تحمل خسارته.
    <br />
    <strong>Risk Warning:</strong> Trading involves high risk and may result in the loss of capital. This project is an educational tool and not investment advice. Do not invest more than you can afford to lose.
  </div>
);

export default RiskWarning;
