pipeline {
    agent {label 'VM_test'}

    stages {
        stage('Check Docker Version') {
            steps {
                script {
                    sh 'java --version'
                }
            }
        }
    }
}