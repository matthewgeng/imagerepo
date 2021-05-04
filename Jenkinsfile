pipeline {
    agent { node { label 'pmqenode' } }
    stages {
        stage('Create Directory') {
            steps {
                echo 'Creating Directory...'
                sh '''ssh -ttt jenkins@mldevapp <<EOF
                mkdir -p /tmp/kyc
                <<EOF
                EOF'''
            }
        }
        stage('Package') {
            steps {
                echo 'Packaging...'
                sh '''scp -r $WORKSPACE/* jenkins@mldevapp:/tmp/kyc'''
                sh '''scp -r $WORKSPACE/.env jenkins@mldevapp:/tmp/kyc'''
                
            }
        }
        stage('Prune') {
            steps {
                echo 'Pruning...'
                sh '''ssh -ttt jenkins@mldevapp <<EOF
                docker stop risk-frontend
                docker stop risk-backend
                docker stop risk-nginx
                <<EOF
                EOF'''
            }
        }
        stage('Build and Deploy') {
            steps {
                echo 'Building and deploying...'
                sh '''ssh -ttt jenkins@mldevapp <<EOF
                cd /tmp/kyc
                docker-compose up --build -d
                <<EOF
                EOF'''
            }
        }
    }
}
