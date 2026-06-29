pipeline {
    agent {
        node {
            label 'selenium-jenkins'
        }
    }

    triggers {
        pollSCM('*/5 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies...'

                sh '''
                    cd myapp

                    python3 -m venv venv

                    . venv/bin/activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium Tests...'

                sh '''
                    cd myapp

                    . venv/bin/activate

                    pytest -v
                '''
            }
        }

        stage('Deliver') {
            steps {
                echo 'Delivery completed.'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '**/reports/*.xml'
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}