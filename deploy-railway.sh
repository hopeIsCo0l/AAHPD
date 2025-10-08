#!/bin/bash

# Railway Deployment Script for Academic Assignment Helper

echo "🚀 Railway Deployment for Academic Assignment Helper"
echo "===================================================="

echo ""
echo "STEP 1: Login to Railway"
echo "Please run this command:"
echo "npx @railway/cli login"
echo ""
echo "This will open a browser window for authentication."
read -p "Press Enter after you've completed the login..."

echo ""
echo "STEP 2: Initialize Railway Project"
echo "Running: npx @railway/cli init"
npx @railway/cli init

echo ""
echo "STEP 3: Add PostgreSQL Database"
echo "Running: npx @railway/cli add postgresql"
npx @railway/cli add postgresql

echo ""
echo "STEP 4: Set Environment Variables"
echo "You need to set these environment variables:"
echo ""
echo "1. OPENAI_API_KEY - Your OpenAI API key"
echo "2. JWT_SECRET_KEY - A random secret key for JWT tokens"
echo ""
echo "Run these commands (replace with your actual values):"
echo "npx @railway/cli variables set OPENAI_API_KEY=your_openai_key_here"
echo "npx @railway/cli variables set JWT_SECRET_KEY=your_jwt_secret_here"
echo ""
read -p "Press Enter after you've set the environment variables..."

echo ""
echo "STEP 5: Deploy Application"
echo "Running: npx @railway/cli up"
npx @railway/cli up

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "Your application should now be deployed on Railway."
echo "Check the Railway dashboard at: https://railway.app/dashboard"
echo ""
echo "The application will be available at the URL shown in the terminal."
echo ""
