// src/components/icons.jsx
import React from 'react';

// 1. 사람 아이콘 (회원정보)
export const UserIcon = ({ size = 24, color = "#325b47  ", className = "" }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className}>
        <circle cx="12" cy="8" r="4" stroke={color} strokeWidth="2" strokeLinecap="round" />
        <path d="M4 20C4 17.7909 5.79086 16 8 16H16C18.2091 16 20 17.7909 20 20" stroke={color} strokeWidth="2" strokeLinecap="round" />
    </svg>
);