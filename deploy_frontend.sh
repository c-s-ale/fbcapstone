echo "Deploying Front End"
cd spotify-frontend
npm run build
aws s3 sync build s3://s2t-frontend-bucket/ --acl public-read