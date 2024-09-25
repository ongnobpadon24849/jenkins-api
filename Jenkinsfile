pipeline {
    agent none
    stages {
        stage('Agent Test Server') {
            agent { label 'VM_test' }

            stages {
                stage("Clone Repository From Jenkins On GitLab") {
                    steps {
                        script {
                            withCredentials([usernamePassword(credentialsId: "Gitlab_ongnobpadon24849", 
                                                            usernameVariable: "GIT_USERNAME", 
                                                            passwordVariable: "GIT_PASSWORD")]) {
                                if (fileExists('jenkins')) {
                                    dir('jenkins') {
                                        sh "git pull origin main"
                                    }
                                } else {
                                    sh "git clone https://${GIT_PASSWORD}@gitlab.com/softdevthree/jenkins.git ."
                                }
                            }
                        }
                    }
                }

                stage("Unit Test") {
                    steps {
                        script {
                            dir('jenkins') {
                                sh '''
                                    . /home/test/robotenv/bin/activate
                                    python3 /home/test/workspace/TestAndDeploy/jenkins/functiontest.py
                                    '''
                            }
                        }
                    }
                }
                
                stage("Build Docker Image") {
                    steps {
                        script {
                            dir('flask_api') {
                                sh '''
                                . /home/test/robotenv/bin/activate
                                python3 /home/test/docker_rm.py
                                '''
                                sh "docker build -t flask-app ."
                            }
                        }
                    }
                }

                stage("Run Docker Container") {
                    steps {
                        script {
                            sh "docker ps -a -q -f name=flask-app | xargs -r docker rm -f"
                            sh "docker run -d --name flask-app -p 8080:5000 flask-app"
                        }
                    }
                }

                stage("Clone Repository From robot_test") {
                    steps {
                        script {
                            withCredentials([usernamePassword(credentialsId: "Gitlab_ongnobpadon24849", 
                                                            usernameVariable: "GIT_USERNAME", 
                                                            passwordVariable: "GIT_PASSWORD")]) {
                                if (fileExists('robot_test')) {
                                    dir('robot_test') {
                                        sh "git pull origin main"
                                    }
                                } else {
                                    sh "git clone https://${GIT_PASSWORD}@gitlab.com/softdevthree/robot_test.git ."
                                }
                            }
                        }
                    }
                }

                stage("Run Robot-Test") {
                    steps {
                        dir('robot_test') {
                            script {
                                sh '''
                                    . /home/test/robotenv/bin/activate
                                    robot /home/test/workspace/TestAndDeploy/robot_test/test-plus.robot
                                    python3 /home/test/docker_stop.py
                                    '''
                            }
                        }
                    }
                }

                stage('Push Docker Image') {
                    steps {
                        script {
                            withCredentials([usernamePassword(credentialsId: "Gitlab_ongnobpadon24849", 
                                                            usernameVariable: "GIT_USERNAME", 
                                                            passwordVariable: "GIT_PASSWORD")]) {
                                sh "docker login -u ${GIT_USERNAME} -p ${GIT_PASSWORD} registry.gitlab.com"
                                sh "docker tag flask-app registry.gitlab.com/softdevthree/jenkins"
                                sh "docker push registry.gitlab.com/softdevthree/jenkins"
                            }
                        }
                    }
                }
            }
        }

        stage('Agent Pre-Prod Server') {
            agent { label 'VM_preprod' }
            
            stages {
                stage("Pull Docker Image") {
                    steps {
                        script {
                            withCredentials([usernamePassword(credentialsId: "Gitlab_ongnobpadon24849", 
                                                            usernameVariable: "GIT_USERNAME", 
                                                            passwordVariable: "GIT_PASSWORD")]) {
                                sh "docker login -u ${GIT_USERNAME} -p ${GIT_PASSWORD} registry.gitlab.com"
                                sh "docker pull registry.gitlab.com/softdevthree/jenkins"
                            }
                        }
                    }
                }

                stage("Run Docker Container") {
                    steps {
                        script {
                            sh '''
                                . /home/preprod/myenv/bin/activate
                                python3 /home/preprod/docker_rm.py
                                '''
                            sh "docker run -d --name flask-app -p 8080:5000 registry.gitlab.com/softdevthree/jenkins"
                        }
                    }
                }
            }
        }
    }
}